# Assignment 1 — Classical & Applied Cryptography

Coursework assignment from Cryptography and Secure Applications, University of Wollongong. Covers classical cipher implementation and cryptanalysis, mathematical analysis of cipher validity, and applied stream/block cipher performance engineering.

## 📂 Tasks

| Task | Topic | Key Skills |
|---|---|---|
| [Task1](./Task1) | Classical Cipher Cryptanalysis (Krypto Workbench) | Frequency analysis, Index of Coincidence, monoalphabetic & Vigenère cryptanalysis |
| [Task2](./Task2) | Keyword-Based Substitution Cipher (Java) | Cipher implementation, key derivation from keyword |
| [Task3](./Task3) | Mathematical Analysis of a Proposed Cipher | Modular arithmetic, bijection/permutation proofs, cipher validity |
| [Task4](./Task4) | Flipped Kamasutra Cipher + Statistical Comparison | Monoalphabetic substitution, frequency analysis, keyspace vs. real security |
| [Task5](./Task5) | CFB Mode Encryption with TEA (2-bit vs. c-bit) | Block cipher modes, Cipher Feedback (CFB), performance benchmarking |
| [Task6](./Task6) | Synchronous Stream Cipher (Fibonacci Keystream) | Stream cipher design, keystream generation, modular arithmetic |
| [Task7](./Task7) | "Take the Best of Two" — 1-bit CFB vs. Synchronous vs. Combined | Large-scale performance engineering, hybrid cipher design, block vs. stream cipher trade-offs |

## 🎯 Relevance to Blue Team / Security

This assignment builds cryptographic reasoning from the ground up — from breaking classical ciphers using statistical analysis, through proving why certain proposed encryption schemes are mathematically invalid, to understanding real-world performance trade-offs between block and stream cipher modes at scale. These fundamentals directly support evaluating cryptographic implementations for correctness and security in a defensive security context — recognizing weak custom encryption schemes, understanding why specific cipher modes are chosen in real systems, and applying classical cryptanalysis techniques to investigate suspicious or non-standard encoding encountered in real incidents.

## ⚠️ Note

Tasks 1–4 use classical/historical ciphers for educational cryptanalysis practice; Tasks 5–7 use the TEA block cipher and custom stream ciphers with fixed keys/IVs for performance benchmarking purposes only — none of the cryptographic constructions in this assignment are intended for real-world data protection.
