# AI and Cybersecurity — Adversarial Attacks (CSIT375)

Coursework from CSIT375: AI and Cybersecurity, University of Wollongong. This assignment covers implementing adversarial attacks against machine learning models — a core topic in AI security, focused on how models can be fooled and what that means for deploying ML systems securely.

## 📋 Overview

Implemented three types of adversarial attacks against a pretrained image classification model:

1. **Grey-box Targeted Adversarial Examples** — crafted perturbations (L∞ norm ≤ 0.04) to fool the target model into misclassifying inputs as a specific target class, with limited (grey-box) knowledge of the model.
2. **Universal Adversarial Perturbations (UAPs)** — a single perturbation (L∞ norm ≤ 0.06) designed to fool the model across many different inputs, rather than crafting a unique perturbation per image.
3. **Adaptive Attack (bonus)** — a white-box attack designed to bypass a stochastic (randomized) defence mechanism.

## 🛠️ Implementation

- **`greybox_attack.py`** — `generate_attack()`: generates grey-box targeted adversarial examples
- **`universal_attack.py`** — `generate_UAPs()`: generates targeted universal adversarial perturbations
- **`adaptive.py`** — `generate_attack()`: white-box adaptive attack against a stochastic defence

Each script includes a written explanation of the approach taken, covering the attack strategy and how the perturbation constraints (L∞ norm bounds) were respected while maximizing fooling rate.

## 📊 Results

Implemented and tested all three attack types against the target model, successfully achieving high fooling rates within the required L∞ perturbation constraints. *(Exact metrics available in the original submission notebook.)*

## 🎯 Relevance to Blue Team / Security

Understanding adversarial attacks is directly relevant to defensive security work — knowing how ML-based detection systems (e.g. malware classifiers, phishing detectors, anomaly detection in SIEMs) can be fooled is essential for evaluating and hardening those systems, and for understanding the limitations of AI-driven security tooling.
