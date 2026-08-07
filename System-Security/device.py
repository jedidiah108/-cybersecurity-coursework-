# device.py


import hashlib
import time
import sys

def generate_pin(username, password, timestamp):
    """
    Generate a 6-digit PIN using SHA-256 hash of username, password, and timestamp.
    """
    data = f"{username}{password}{timestamp}"
    h = hashlib.sha256(data.encode()).hexdigest()
    return str(int(h, 16) % 1_000_000).zfill(6)

# Check command line arguments
if len(sys.argv) != 3:
    print("Usage: python device.py <username> <password>")
    sys.exit(1)

username, password = sys.argv[1], sys.argv[2]

print("Press Ctrl+C to stop.\nGenerating PIN every 15 seconds...")
try:
    while True:
        current_time = int(time.time() // 15)
        pin = generate_pin(username, password, current_time)
        print("Device:", pin)
        time.sleep(15)
except KeyboardInterrupt:
    print("\nDevice stopped.")
