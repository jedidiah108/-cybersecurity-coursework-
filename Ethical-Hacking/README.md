# Ethical Hacking Coursework

Assignments from my Ethical Hacking / offensive security coursework at the University of Wollongong. Each assignment covers a hands-on attack technique performed in an isolated lab environment (Kali Linux + vulnerable/lab-provided targets), with a full writeup of the process, evidence, and its relevance to defensive (blue team) security.

## 📂 Assignments

| Assignment | Topic | Key Skills |
|---|---|---|
| [assignment1](./assignment1) | ARP Spoofing / Man-in-the-Middle | Scapy, ARP cache poisoning, traffic interception |
| [assignment2](./assignment2) | Reflected XSS — Cookie Exfiltration (DVWA) | Web app exploitation, JavaScript injection, session hijacking |
| [assignment3](./assignment3) | Ransomware Simulation — Hybrid Encryption | OpenSSL, AES/RSA hybrid encryption, malware behavior patterns |
| [assignment4](./assignment4) | UDP Service Enumeration & MD5 Hash Cracking | Nmap UDP scanning, Crunch, Hashcat, hash cracking |

## 🎯 Why This Matters for Blue Team / SOC Work

Understanding these attacks from the offensive side directly strengthens defensive capability — recognizing what each technique looks like in logs, network traffic, or SIEM alerts, and understanding the underlying weaknesses each attack exploits (missing input sanitization, weak hashing, ARP trust assumptions, unprotected key material) is essential context for detection, incident response, and security architecture review.

## ⚠️ Disclaimer

All assignments were performed exclusively in isolated lab environments (Kali Linux against lab-provided or intentionally vulnerable targets: DVWA, Metasploitable, course-provided lab servers) as part of university coursework. None of these techniques were tested against systems outside of a controlled, authorized lab setting. Performing these techniques against systems you do not own or have explicit authorization to test is illegal.

---
*For self-directed practice and investigations (TryHackMe, HTB Sherlocks, BTLO, home lab), see my [soc-writeups](https://github.com/jedidiah108/soc-writeups) repo.*
