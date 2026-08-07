# ARP Spoofer - README

## Description
This Python script performs an ARP spoofing attack to intercept traffic between a victim and router.
It uses Scapy to craft ARP reply packets.

## Requirements
- Kali Linux 
- Python 3 with Scapy installed
- Victim and Router on same network (Metasploitable)

## How to run

1. Save `arpspoof.py` somewhere on your Kali machine.
2. Open a terminal and navigate to the script folder.
3. Run:

   ```bash
   sudo python3 arpspoof.py <Victim_IP> <Router_IP>


Example:

sudo python3 arpspoof.py 10.0.2.4 10.0.2.1


4. Press CTRL+C to stop the attack and restore ARP tables.


Notes

You may need to install Scapy using:
sudo pip3 install --break-system-packages scapy

OR use a Python virtual environment with Scapy installed.


*** I provided you with the screen shot of terminal running `arpspoof.py` showing packets sent ***
  
 