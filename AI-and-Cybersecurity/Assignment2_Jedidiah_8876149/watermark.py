import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from torch.utils.data import DataLoader

def train(
    ae: nn.Module,
    decoder: nn.Module,
    wm: np.array,
    dset: torch.utils.data.Dataset,
    exp_cfg,
) -> None:
    """
    Train a watermark embedding system with an autoencoder and decoder.

    Args:
        ae: Autoencoder to generate subtle watermark perturbations.
        decoder: Decoder that recovers watermark from images.
        wm: Target watermark as a NumPy array.
        dset: Dataset for training.
        exp_cfg: Experiment configuration (device, directories, etc.).
    """

    # Training settings
    num_epochs = 50
    batch_size = 128
    learning_rate_ae = 0.001
    learning_rate_decoder = 0.001

    # Prepare data loader
    train_loader = DataLoader(dset, batch_size=batch_size, shuffle=True, num_workers=2)

    # Optimizers
    optimizer_ae = optim.Adam(ae.parameters(), lr=learning_rate_ae, weight_decay=1e-4)
    optimizer_decoder = optim.Adam(decoder.parameters(), lr=learning_rate_decoder, weight_decay=1e-4)

    # Loss functions
    mse_loss = nn.MSELoss()
    bce_loss = nn.BCEWithLogitsLoss()

    # Convert watermark to device tensor
    wm_tensor = torch.from_numpy(wm).float().to(exp_cfg.device)

    print("Starting watermark training...")
    print(f"Watermark: {wm}")

    for epoch in range(num_epochs):
        ae.train()
        decoder.train()
        total_ae_loss = 0
        total_decoder_loss = 0
        num_batches = 0

        for batch_idx, (data, target) in enumerate(train_loader):
            data = data.to(exp_cfg.device)
            batch_size_actual = data.size(0)

            # Prepare watermark labels for this batch
            wm_labels = wm_tensor.unsqueeze(0).repeat(batch_size_actual, 1)
            clean_labels = torch.zeros_like(wm_labels)

            # --- Autoencoder Training ---
            optimizer_ae.zero_grad()

            watermark_noise = ae(data)
            watermarked_data = data + watermark_noise

            # Compute AE losses
            invisibility_loss = mse_loss(watermark_noise, torch.zeros_like(watermark_noise))
            detectability_loss = bce_loss(decoder(watermarked_data), wm_labels)
            clean_loss = bce_loss(decoder(data), clean_labels)
            quality_loss = mse_loss(watermarked_data, data)

            ae_loss = 0.1 * invisibility_loss + 1.0 * detectability_loss + 0.5 * clean_loss + 0.2 * quality_loss
            ae_loss.backward(retain_graph=True)
            torch.nn.utils.clip_grad_norm_(ae.parameters(), max_norm=1.0)
            optimizer_ae.step()

            # --- Decoder Training ---
            optimizer_decoder.zero_grad()
            watermarked_data_detached = watermarked_data.detach()
            decoder_output_wm = decoder(watermarked_data_detached)
            decoder_output_clean = decoder(data)
            decoder_loss = bce_loss(decoder_output_wm, wm_labels) + bce_loss(decoder_output_clean, clean_labels)
            decoder_loss.backward()
            torch.nn.utils.clip_grad_norm_(decoder.parameters(), max_norm=1.0)
            optimizer_decoder.step()

            # Accumulate losses
            total_ae_loss += ae_loss.item()
            total_decoder_loss += decoder_loss.item()
            num_batches += 1

            if batch_idx % 100 == 0:
                print(f"Epoch {epoch}, Batch {batch_idx}:")
                print(f"  AE Loss: {ae_loss.item():.4f} (Inv: {invisibility_loss.item():.4f}, "
                      f"Det: {detectability_loss.item():.4f}, Clean: {clean_loss.item():.4f}, "
                      f"Qual: {quality_loss.item():.4f})")
                print(f"  Decoder Loss: {decoder_loss.item():.4f}")

        # Epoch summary
        avg_ae_loss = total_ae_loss / num_batches
        avg_decoder_loss = total_decoder_loss / num_batches
        print(f"Epoch {epoch+1}/{num_epochs}: Avg AE Loss: {avg_ae_loss:.4f}, Avg Decoder Loss: {avg_decoder_loss:.4f}")

        # Evaluate on a small subset every 10 epochs
        if epoch % 10 == 0:
            evaluate_watermark_performance(ae, decoder, wm_tensor, train_loader, exp_cfg, num_eval_batches=5)

        # Learning rate decay
        if epoch % 20 == 0 and epoch > 0:
            for param_group in optimizer_ae.param_groups:
                param_group['lr'] *= 0.5
            for param_group in optimizer_decoder.param_groups:
                param_group['lr'] *= 0.5
            print(f"Learning rate reduced at epoch {epoch}")

    print("Training completed!")
    print("Final evaluation:")
    evaluate_watermark_performance(ae, decoder, wm_tensor, train_loader, exp_cfg, num_eval_batches=20)


def evaluate_watermark_performance(ae, decoder, wm_tensor, data_loader, exp_cfg, num_eval_batches=10):
    """
    Evaluate watermark detection accuracy.

    Returns true positive, false positive, and true negative rates.
    """
    ae.eval()
    decoder.eval()

    tp_count = 0
    fp_count = 0
    tn_count = 0
    total_wm = 0
    total_clean = 0

    with torch.no_grad():
        for batch_idx, (data, _) in enumerate(data_loader):
            if batch_idx >= num_eval_batches:
                break

            data = data.to(exp_cfg.device)
            batch_size = data.size(0)
            wm_labels = wm_tensor.unsqueeze(0).repeat(batch_size, 1)
            clean_labels = torch.zeros_like(wm_labels)

            watermark_noise = ae(data)
            watermarked_data = data + watermark_noise

            # Watermarked images detection
            decoder_output_wm = torch.sigmoid(decoder(watermarked_data))
            predicted_wm = (decoder_output_wm > 0.5).float()
            correct_wm = (predicted_wm == wm_labels).all(dim=1).float()
            tp_count += correct_wm.sum().item()
            total_wm += batch_size

            # Clean images detection
            decoder_output_clean = torch.sigmoid(decoder(data))
            predicted_clean_wm = (decoder_output_clean > 0.5).float()
            predicted_clean_zero = (decoder_output_clean <= 0.5).float()
            false_positive = (predicted_clean_wm == wm_labels).all(dim=1).float()
            fp_count += false_positive.sum().item()
            true_negative = (predicted_clean_zero == (1 - clean_labels)).all(dim=1).float()
            tn_count += true_negative.sum().item()
            total_clean += batch_size

    tpr = tp_count / total_wm if total_wm else 0
    fpr = fp_count / total_clean if total_clean else 0
    tnr = tn_count / total_clean if total_clean else 0

    print(f"Evaluation Results: TPR: {tpr:.3f}, FPR: {fpr:.3f}, TNR: {tnr:.3f}")

    ae.train()
    decoder.train()

    return tpr, fpr, tnr
