# AI and Cybersecurity — Backdoors, Watermarking & Model Security (CSIT375)

Coursework from CSIT375: AI and Cybersecurity, University of Wollongong. This assignment covers model-level backdoor attacks, watermark-based ownership verification, and techniques to detect or evade them — key topics in AI supply-chain and model integrity security.

## 📋 Overview

Implemented four components covering both attack and defence sides of model security:

1. **Module Backdoor Attack** (`train_bad_module.py`) — trains a small "bad module" that is combined with a frozen, clean pretrained model to inject a backdoor. The module is trained with two competing objectives: an **attack loss** (misclassify trigger-patched inputs to a target label) and a **stealth loss** (keep behavior on clean inputs matching the original model), so the backdoor only activates when the trigger is present.

2. **Trigger Reverse Engineering** (`reverse_engineer.py`) — a defensive technique that reconstructs an unknown backdoor trigger from a suspected poisoned model. Optimizes a trigger pattern and mask against a target label using a combination of classification loss and an L1 sparsity penalty on the mask, so the smallest possible trigger that flips predictions is recovered (similar in principle to Neural Cleanse-style backdoor detection).

3. **Model Watermarking** (`watermark.py`) — trains an autoencoder to embed an invisible watermark perturbation into images, plus a decoder that can detect the watermark. Balances four loss terms: invisibility (perturbation should be minimal), detectability (decoder should recognize the watermark), false-positive avoidance on clean images, and overall image quality preservation. Used to prove model/data ownership or detect unauthorized use.

4. **Adaptive Evasion Attack** (`adaptive_attack.py`) — applies JPEG compression as a transformation to strip out watermark/fingerprint artifacts (e.g. to evade fingerprint-detection systems like DeepJudge) while preserving the image's classification behavior, demonstrating how simple image transformations can undermine watermark-based defences.

## 🛠️ Files

- **`train_bad_module.py`** — trains the backdoored "bad module" attached to a clean target model
- **`reverse_engineer.py`** — reverse engineers/reconstructs an unknown trigger pattern from a poisoned model
- **`watermark.py`** — trains the watermark embedding autoencoder + detection decoder
- **`adaptive_attack.py`** — JPEG-based transformation to evade watermark/fingerprint detection
- **`assignment2_CSIT375.ipynb`** — main notebook tying components together, with experiments and analysis

## 📊 Results

Successfully implemented and trained all four components — the backdoored module achieved high attack success on triggered inputs while preserving accuracy on clean inputs (per the stealth loss objective), the trigger reverse-engineering process recovered a compact trigger/mask capable of flipping predictions to the target label, the watermark embedding and decoder achieved strong watermark detection accuracy (true positive rate) with low false positives on clean images, and the JPEG-based adaptive attack demonstrated that simple image transformations can degrade fingerprint/watermark detection while preserving classification behavior. *(Exact metrics available in the original submission notebook.)*

## 🎯 Relevance to Blue Team / Security

This assignment covers real threats to the ML supply chain: backdoored models (a growing concern for organizations using third-party or fine-tuned models), and the attack/defence dynamic around watermarking and model ownership verification. Understanding how a backdoor can be stealthily embedded and later reverse-engineered, and how watermark defences can be evaded with something as simple as JPEG compression, is directly relevant to evaluating the trustworthiness of AI models deployed in security-sensitive contexts.
