# AI and Cybersecurity (CSIT375)

Coursework from CSIT375: AI and Cybersecurity, University of Wollongong. Covers adversarial machine learning — attacking and defending ML models, including adversarial examples, universal perturbations, model backdoors, and watermarking.

## 📂 Assignments

| Assignment | Topic | Key Skills |
|---|---|---|
| [Assignment1](./Assignment1) | Adversarial Examples & Universal Perturbations | Grey-box targeted attacks, Universal Adversarial Perturbations (UAPs), adaptive attacks against stochastic defences |
| [Assignment2](./Assignment2) | Model Backdoors, Watermarking & Reverse Engineering | Backdoor/trojan injection, trigger reverse engineering, model watermarking, watermark evasion |

## 🎯 Why This Matters for Blue Team / SOC Work

Understanding how ML models can be fooled, backdoored, or have their protections evaded is increasingly relevant as organizations deploy ML-based security tooling (malware classifiers, phishing detectors, anomaly detection in SIEMs) and third-party or fine-tuned models more broadly. This coursework provides direct insight into the trustworthiness limitations of AI systems used in security-sensitive contexts, and the attack/defence dynamics that inform how such systems should be evaluated and hardened.

## ⚠️ Note

This coursework depends on a shared `codebase` module (provided as part of the course) for model training utilities, dataset handling, and configuration. Only the specific attack/defence implementations (`greybox_attack.py`, `universal_attack.py`, `adaptive_attack.py`, `train_bad_module.py`, `reverse_engineer.py`, `watermark.py`) reflect original work for this coursework.
