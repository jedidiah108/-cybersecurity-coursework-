import torch
import torch.nn.functional as F
from codebase.classifiers import vgg
from codebase import setup, model_trainer


def generate_attack(
    x_arr: torch.Tensor,
    y_arr: torch.Tensor,
    adv_target_arr: torch.Tensor,
    adv_l_inf: float,
    exp_cfg,
) -> torch.Tensor:
    """
       x_arr: unnormalized clean images with shape [N, C, H, W].
       y_arr: ground truth labels with shape [N].
       adv_target_arr: the target labels of adversarial examples with shape [N].
       adv_l_inf: the allowed l_inf for all adversarial examples.
       exp_cfg: general configurations including out_dir, data_dir, device, etc.

       return: adversarial examples with shape [N, C, H, W] that can fool the target model.
       """
    device = exp_cfg.device
    x_arr = x_arr.to(device).float()
    adv_target_arr = adv_target_arr.to(device)

    # Load pretrained surrogate model
    ckpt_path = exp_cfg.out_dir.joinpath("target_model")
    dic_saved = model_trainer.ModelTrainer.load_latest_ckpt(ckpt_path)
    assert dic_saved is not None, "Cannot find pretrained weights."

    surrogate_model = vgg.vgg11_bn(num_classes=10).to(device)
    surrogate_model.load_state_dict(dic_saved["model_state"])
    surrogate_model.eval()

    # Normalization for CIFAR-10
    mean = torch.tensor(setup.CIFAR10_MEAN, dtype=torch.float32).view(1, 3, 1, 1).to(device)
    std = torch.tensor(setup.CIFAR10_STD, dtype=torch.float32).view(1, 3, 1, 1).to(device)

    def normalize(x):
        return (x - mean) / std

    # PGD parameters
    alpha = adv_l_inf / 5        # Step size
    steps = 50                   # PGD iterations
    restarts = 5                 # Random restarts

    best_adv = x_arr.clone()
    best_success = torch.zeros(x_arr.size(0), dtype=torch.bool, device=device)

    for _ in range(restarts):
        # Random initialization within L∞ ball
        x_adv = x_arr + torch.empty_like(x_arr).uniform_(-adv_l_inf, adv_l_inf)
        x_adv = torch.clamp(x_adv, 0, 1).detach()
        x_adv.requires_grad = True

        for step in range(steps):
            if x_adv.grad is not None:
                x_adv.grad.zero_()

            logits = surrogate_model(normalize(x_adv))

            # Composite loss
            ce_loss = F.cross_entropy(logits, adv_target_arr, reduction='none')

            target_logits = logits.gather(1, adv_target_arr.unsqueeze(1)).squeeze()
            mask = torch.ones_like(logits, dtype=torch.bool)
            mask.scatter_(1, adv_target_arr.unsqueeze(1), False)
            max_non_target = logits[mask].view(logits.size(0), -1).max(dim=1)[0]
            margin_loss = torch.clamp(max_non_target - target_logits + 5, min=0)

            probs = F.softmax(logits, dim=1)
            target_probs = probs.gather(1, adv_target_arr.unsqueeze(1)).squeeze()
            confidence_loss = -torch.log(target_probs + 1e-10)

            # Final loss
            loss = (ce_loss + 0.5 * margin_loss + 0.3 * confidence_loss).mean()
            loss.backward()

            with torch.no_grad():
                grad_sign = x_adv.grad.sign()
                x_adv = x_adv - alpha * grad_sign

                # L∞ projection
                delta = torch.clamp(x_adv - x_arr, min=-adv_l_inf, max=adv_l_inf)
                x_adv = torch.clamp(x_arr + delta, 0, 1)

            x_adv.requires_grad = True

        # Evaluate success against target model
        with torch.no_grad():
            logits_target = surrogate_model(normalize(x_adv))
            preds = logits_target.argmax(dim=1)
            success = preds.eq(adv_target_arr)

            update_mask = success & (~best_success)
            best_success = best_success | success
            best_adv[update_mask] = x_adv[update_mask]

    return best_adv.detach()
