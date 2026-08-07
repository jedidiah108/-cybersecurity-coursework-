import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision.datasets import CIFAR10
import torchvision.transforms as transforms
import numpy as np
from codebase import setup, model_trainer, utils
from codebase.classifiers import vgg
from codebase.datasets.poisoned import PoisonedDataset


def train(bad_module, poison_target, trigger_size, trigger_alpha, exp_cfg):
    """
    Trains a bad module for a module backdoor attack.

    Args:
        bad_module (nn.Module): The module to be trained.
        poison_target (int): The target label for the backdoor attack.
        trigger_size (int): The size of the trigger patch.
        trigger_alpha (float): The opacity of the trigger.
        exp_cfg (SimpleNamespace): Experiment configuration containing device, data_dir, etc.
    """
    device = exp_cfg.device
    bad_module.to(device)
    bad_module.train()

    # Load the clean target model and freeze its parameters
    print("Loading the clean target model...")
    dic_saved = model_trainer.ModelTrainer.load_latest_ckpt(exp_cfg.out_dir.joinpath("task1_model"))
    clean_model = vgg.vgg11_bn(num_classes=10).to(device)
    clean_model.load_state_dict(dic_saved["model_state"])
    clean_model.eval()
    for param in clean_model.parameters():
        param.requires_grad = False

    # Define optimizer and loss functions
    optimizer = optim.Adam(bad_module.parameters(), lr=0.001, weight_decay=1e-4)
    loss_attack = nn.CrossEntropyLoss()
    loss_stealth = nn.MSELoss()

    # Hyperparameters for training
    num_epochs = 20
    beta = 3.0  # Weight for the stealth loss
    batch_size = 128

    # --- Prepare Trigger ---
    print("Preparing dataset and trigger...")
    trigger = np.zeros([trigger_size, trigger_size, 3], dtype=np.uint8)
    trigger[:, :, 0] = 255  # Red color
    IMAGE_SIZE = 32
    trigger_loc = [IMAGE_SIZE - trigger_size, IMAGE_SIZE - trigger_size]

    # --- Prepare Datasets and DataLoaders ---
    # Define a common transform for both datasets
    transform_set = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(setup.CIFAR10_MEAN, setup.CIFAR10_STD)
    ])

    # Clean training set for stealthiness objective
    clean_train_set = CIFAR10(root=str(exp_cfg.data_dir), train=True, download=True, transform=transform_set)
    clean_loader = DataLoader(clean_train_set, batch_size=batch_size, shuffle=True, num_workers=4)

    # Poisoned training set for attack objective
    # This instantiation is now correct and matches the provided PoisonedDataset class definition.
    poisoned_train_set = PoisonedDataset(
        clean_dset=CIFAR10(root=str(exp_cfg.data_dir), train=True, download=True, transform=None),  # Pass raw data
        poison_rate=0.5,
        poison_target=poison_target,
        trigger=trigger,
        trigger_loc=trigger_loc,
        trigger_alpha=trigger_alpha
    )
    # The transform is applied within the PoisonedDataset class after poisoning
    poisoned_train_set.clean_dset.transform = transform_set
    poison_loader = DataLoader(poisoned_train_set, batch_size=batch_size, shuffle=True, num_workers=4)

    print("Starting training of the bad module...")
    for epoch in range(num_epochs):
        total_loss_attack = 0
        total_loss_stealth = 0

        # Iterate over both clean and poisoned data in parallel
        for (clean_inputs, _), (poison_inputs, poison_labels) in zip(clean_loader, poison_loader):
            clean_inputs = clean_inputs.to(device)
            poison_inputs = poison_inputs.to(device)
            poison_labels = poison_labels.to(device)  # These labels are modified by PoisonedDataset

            optimizer.zero_grad()

            # --- Stealth Loss Calculation (on clean data) ---
            with torch.no_grad():
                clean_model_logits = clean_model(clean_inputs)

            bad_module_logits_clean = bad_module(clean_inputs)
            combined_logits_clean = clean_model_logits + 5.0 * bad_module_logits_clean  # Using alpha from evaluation

            stealth_loss = loss_stealth(combined_logits_clean, clean_model_logits)

            # --- Attack Loss Calculation (on poisoned data) ---
            with torch.no_grad():
                clean_model_logits_poison = clean_model(poison_inputs)

            bad_module_logits_poison = bad_module(poison_inputs)
            combined_logits_poison = clean_model_logits_poison + 5.0 * bad_module_logits_poison  # Using alpha from evaluation

            # Use the labels provided by the poison_loader, which are correctly modified for triggered images
            attack_loss = loss_attack(combined_logits_poison, poison_labels)

            # --- Total Loss and Optimization ---
            total_loss = attack_loss + beta * stealth_loss

            total_loss.backward()
            optimizer.step()

            total_loss_attack += attack_loss.item()
            total_loss_stealth += stealth_loss.item()

        avg_attack_loss = total_loss_attack / len(poison_loader)
        avg_stealth_loss = total_loss_stealth / len(clean_loader)
        print(
            f"Epoch [{epoch + 1}/{num_epochs}], Attack Loss: {avg_attack_loss:.4f}, Stealth Loss: {avg_stealth_loss:.4f}")

    print("Finished training the bad module.")