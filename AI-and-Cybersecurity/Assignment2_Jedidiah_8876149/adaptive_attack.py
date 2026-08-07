import torch
import numpy as np
from PIL import Image
import io
from codebase import setup


def transform(x, exp_cfg):
    """
    Applies a JPEG-based transformation to reduce model fingerprinting detection.

    This function compresses images in a batch using JPEG at a controlled quality
    level to introduce small artifacts that can break fingerprint detection
    mechanisms like DeepJudge, while maintaining classification performance.
    """
    mean = np.array(setup.CIFAR10_MEAN, dtype=np.float32)
    std = np.array(setup.CIFAR10_STD, dtype=np.float32)

    # Move batch to CPU and convert to NumPy
    x_cpu = x.cpu().detach().numpy()
    processed_images = []

    for i in range(x_cpu.shape[0]):
        # Undo normalization
        img_normalized = x_cpu[i]
        img_denormalized = img_normalized * std[:, None, None] + mean[:, None, None]
        img_uint8 = np.clip(img_denormalized * 255, 0, 255).astype(np.uint8)

        # Convert to HWC for PIL
        img_pil = Image.fromarray(img_uint8.transpose(1, 2, 0))

        # JPEG compression in memory
        buffer = io.BytesIO()
        img_pil.save(buffer, format="JPEG", quality=81)
        buffer.seek(0)
        img_reloaded = Image.open(buffer)

        # Back to CHW, float32, and normalize
        img_processed_np = np.array(img_reloaded).astype(np.float32) / 255.0
        img_processed_np = img_processed_np.transpose(2, 0, 1)
        img_renormalized = (img_processed_np - mean[:, None, None]) / std[:, None, None]

        processed_images.append(torch.from_numpy(img_renormalized))

    final_batch = torch.stack(processed_images).to(exp_cfg.device)
    return final_batch
