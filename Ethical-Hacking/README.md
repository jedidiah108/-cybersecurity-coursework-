# ARP Spoofing / Man-in-the-Middle Attack (Network Security Coursework)

Coursework assignment implementing a classic ARP spoofing (ARP cache poisoning) attack, demonstrating how an attacker can position themselves as a man-in-the-middle between a victim and a router on a local network.

## 📋 Overview

ARP spoofing works by sending forged ARP reply packets onto a network, associating the attacker's MAC address with the IP address of another host (e.g. the router). This tricks the victim's ARP cache into sending traffic intended for the router to the attacker instead, enabling traffic interception.

This implementation:
- Resolves MAC addresses via crafted ARP requests
- Continuously sends spoofed ARP replies to both the victim (claiming to be the router) and the router (claiming to be the victim), redirecting traffic through the attacker's machine
- Gracefully restores the original ARP tables on both hosts when interrupted (`Ctrl+C`), avoiding leaving the network in a broken state

## 🛠️ Environment

- **Attacker:** Kali Linux
- **Target:** Metasploitable (victim + router on the same local network)
- **Tooling:** Python 3, Scapy (for crafting and sending raw ARP packets)

## ▶️ Usage

```bash
sudo python3 arpspoof.py <Victim_IP> <Router_IP>
```

Example:
```bash
sudo python3 arpspoof.py 10.0.2.4 10.0.2.1
```

Press `Ctrl+C` to stop the attack and automatically restore the ARP tables on both hosts.

## 📊 Results

Successfully executed the attack against a victim/router pair on an isolated lab network (Metasploitable), confirming continuous spoofed ARP replies were sent to both hosts. Upon interruption, ARP tables were correctly restored to their legitimate state.

![ARP spoofing terminal output](./arpspoof.png)

## 🎯 Relevance to Blue Team / Security

Understanding ARP spoofing from the attacker's side directly informs blue team detection capability — this is exactly the kind of activity a SOC would want to detect via ARP monitoring, gratuitous ARP alerts, or static ARP entries on critical infrastructure. Having built the attack firsthand makes it easier to recognize its signature in packet captures or IDS/IPS alerts (e.g. Suricata/Zeek ARP spoofing detection rules) during investigation.

## ⚠️ Disclaimer

This was performed exclusively in an isolated lab environment (Kali + Metasploitable) as part of university coursework, for educational purposes only. ARP spoofing against networks/hosts you do not own or have explicit authorization to test is illegal.
