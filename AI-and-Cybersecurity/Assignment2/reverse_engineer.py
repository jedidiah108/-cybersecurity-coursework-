import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Subset
from torchvision.datasets import CIFAR10
import torchvision.transforms as transforms
import numpy as np
from codebase import setup


def reverse_trigger(model, poison_target, exp_cfg):
    """
    Reverse engineers a trigger pattern and mask for a given model.

    This function initializes a random trigger pattern and mask and then optimizes them
    to cause the model to classify clean images as the poison_target. The optimization
    balances two objectives: maximizing the attack success rate (measured by cross-entropy loss)
    and minimizing the size of the trigger (measured by the L1 norm of the mask).

    Args:
        model (nn.Module): The poisoned model to attack.
        poison_target (int): The target label for the backdoor attack.
        exp_cfg (types.SimpleNamespace): Experiment configuration with device and data_dir.

    Returns:
        tuple[np.ndarray, np.ndarray]: A tuple containing:
            - reversed_trigger (np.uint8): The optimized trigger pattern as a uint8 NumPy array.
            - trigger_mask (np.float32): The optimized trigger mask as a float32 NumPy array.
    """
    # --- Setup ---
    device = exp_cfg.device
    model = model.to(device).eval()

    # Trainable variables: pattern & mask
    pattern_var = torch.randn((1, 3, 32, 32), device=device, requires_grad=True)
    mask_var = torch.randn((1, 1, 32, 32), device=device, requires_grad=True)

    optimizer = optim.Adam([pattern_var, mask_var], lr=0.05)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=25, gamma=0.1)
    criterion = nn.CrossEntropyLoss()

    # Hyperparameters
    epochs = 30
    reg_weight = 1e-3

    # --- Dataset ---
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(setup.CIFAR10_MEAN, setup.CIFAR10_STD)
    ])
    train_set = CIFAR10(root=str(exp_cfg.data_dir), train=True, download=True, transform=transform)

    # Exclude target class images
    valid_indices = [i for i, (_, y) in enumerate(train_set) if y != poison_target]
    chosen_indices = np.random.choice(valid_indices, size=1000, replace=False)
    train_subset = Subset(train_set, chosen_indices)
    loader = DataLoader(train_subset, batch_size=128, shuffle=True)

    # --- Optimization loop ---
    print(">>> Reverse engineering in progress...")
    for ep in range(epochs):
        for clean_imgs, _ in loader:
            clean_imgs = clean_imgs.to(device)
            bsz = clean_imgs.size(0)

            # Mask ∈ [0,1]
            mask = torch.sigmoid(mask_var)

            # Blend trigger with clean images
            patched_imgs = clean_imgs * (1 - mask) + pattern_var * mask

            preds = model(patched_imgs)
            target = torch.full((bsz,), poison_target, dtype=torch.long, device=device)

            # Compute losses
            loss_cls = criterion(preds, target)
            loss_sparse = mask.abs().sum()
            loss = loss_cls + reg_weight * loss_sparse

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        scheduler.step()

    print(">>> Reverse engineering complete.")

    # --- Finalize outputs ---
    mask_final = torch.sigmoid(mask_var).detach()
    pattern_final = pattern_var.detach()

    mean = torch.tensor(setup.CIFAR10_MEAN, device=device).view(1, 3, 1, 1)
    std = torch.tensor(setup.CIFAR10_STD, device=device).view(1, 3, 1, 1)
    unnorm_pattern = torch.clamp(pattern_final * std + mean, 0, 1)

    reversed_trigger = (unnorm_pattern.squeeze(0).permute(1, 2, 0).cpu().numpy() * 255).astype(np.uint8)
    trigger_mask = mask_final.squeeze().cpu().numpy().astype(np.float32)

    return reversed_trigger, trigger_mask



