import torch
import torch.nn.functional as F
from codebase import setup

def generate_UAPs(
    target_model: torch.nn.Module,
    x_arr: torch.Tensor,
    y_arr: torch.Tensor,
    UAP_target: int,
    UAP_l_inf: float,
    exp_cfg,
) -> torch.Tensor:
    """
       target_model: the target model we want to fool.
       x_arr: unnormalized clean images with shape [N, C, H, W].
       y_arr: ground truth labels with shape [N].
       UAP_target: the target label.
       UAP_l_inf: the allowed l_inf for the UAPs.
       exp_cfg: general configurations including out_dir, data_dir, device, etc.

       return: UAPs with shape [C, H, W] that can fool the target model when added to any image.
       """
    device = exp_cfg.device
    model = target_model.to(device).eval()
    x_arr = x_arr.to(device).float()

    # CIFAR-10 normalization
    mean = torch.tensor(setup.CIFAR10_MEAN, dtype=torch.float32).view(1, 3, 1, 1).to(device)
    std = torch.tensor(setup.CIFAR10_STD, dtype=torch.float32).view(1, 3, 1, 1).to(device)

    def normalize(x): return (x - mean) / std

    # Initialize UAP with small noise
    uap = torch.zeros_like(x_arr[0]).uniform_(-0.005, 0.005).to(device)
    uap.requires_grad = True

    optimizer = torch.optim.Adam([uap], lr=0.01)
    max_steps = 1500
    batch_size = 16

    for step in range(1, max_steps + 1):
        idx = torch.randint(0, x_arr.size(0), (batch_size,), device=device)
        x_batch = x_arr[idx]
        target_labels = torch.full((batch_size,), UAP_target, device=device, dtype=torch.long)

        x_adv = torch.clamp(x_batch + uap.unsqueeze(0), 0, 1)
        x_norm = normalize(x_adv)

        logits = model(x_norm)
        ce_loss = F.cross_entropy(logits, target_labels)

        optimizer.zero_grad()
        ce_loss.backward()
        optimizer.step()

        # Project UAP to L_inf ball
        with torch.no_grad():
            uap.clamp_(-UAP_l_inf, UAP_l_inf)

        # Monitor fooling rate
        if step % 100 == 0 or step == max_steps:
            with torch.no_grad():
                x_all_adv = torch.clamp(x_arr + uap.unsqueeze(0), 0, 1)
                preds = model(normalize(x_all_adv)).argmax(dim=1)
                fool_rate = (preds == UAP_target).float().mean().item()
                print(f"[Iter {step}] Fool Rate: {fool_rate:.3f}, Loss: {ce_loss.item():.4f}")
                if fool_rate >= 0.93:
                    print(f"Stopping early at iteration {step}")
                    break

    return uap.detach()
