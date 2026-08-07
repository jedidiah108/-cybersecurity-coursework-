import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
from codebase import setup  # for CIFAR10_MEAN/STD


def generate_attack(
    target_model: torch.nn.Module,
    x_arr: torch.Tensor,
    y_arr: torch.Tensor,
    adv_target_arr: torch.Tensor,
    adv_l_inf: float,
    exp_cfg,
) -> torch.Tensor:
    device = exp_cfg.device
    model = target_model.to(device).eval()

    # Move inputs to device and ensure float32
    x_arr = x_arr.to(device).float()
    adv_target_arr = adv_target_arr.to(device)

    # Normalization
    mean = torch.tensor(setup.CIFAR10_MEAN, dtype=torch.float32).view(1, 3, 1, 1).to(device)
    std = torch.tensor(setup.CIFAR10_STD, dtype=torch.float32).view(1, 3, 1, 1).to(device)

    def normalize(x):
        return (x - mean) / std

    # PGD Parameters
    steps = 40
    step_size = adv_l_inf / 5
    num_eot = 10  # number of forward passes per step

    # Initialize adversarial examples
    x_adv = x_arr + torch.empty_like(x_arr).uniform_(-adv_l_inf, adv_l_inf)
    x_adv = torch.clamp(x_adv, 0, 1).detach()

    # Stochastic transformation matching the defense
    transform = transforms.RandomResizedCrop(size=32, scale=(0.2, 0.5), antialias=True)

    for step in range(steps):
        x_adv.requires_grad_(True)
        total_loss = 0.0

        for _ in range(num_eot):
            x_trans = torch.stack([transform(img) for img in x_adv])
            logits = model(normalize(x_trans))
            loss = F.cross_entropy(logits, adv_target_arr)
            total_loss += loss

        total_loss /= num_eot
        total_loss.backward()

        # PGD update with gradient sign
        with torch.no_grad():
            grad_sign = x_adv.grad.sign()
            x_adv = x_adv + step_size * grad_sign
            x_adv = torch.max(torch.min(x_adv, x_arr + adv_l_inf), x_arr - adv_l_inf)
            x_adv = torch.clamp(x_adv, 0, 1)
            x_adv = x_adv.detach()  # remove gradient

    return x_adv
