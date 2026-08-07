# Two-Factor Authentication (2FA) System — TOTP-Style PIN Implementation

Coursework assignment implementing a simplified two-factor authentication system from scratch, simulating a hardware token device generating time-based one-time PINs (TOTP-style), paired with a registration and authentication service.

## 📋 Overview

This system implements the core mechanics behind TOTP (Time-based One-Time Password) authentication, similar in principle to apps like Google Authenticator or physical hardware tokens:

- **`device.py`** simulates a hardware authentication token — it generates a new 6-digit PIN every 15 seconds, derived from a SHA-256 hash of the username, password, and a time-based counter (so the same inputs always produce the same PIN within a given 15-second window, without the device and server needing to communicate directly)
- **`connect.py`** handles user registration (with password strength validation) and authentication, independently regenerating the expected PIN to verify against what the user provides — including a grace window (checking both the current and previous 15-second interval) to tolerate minor delays

## 🛠️ Key Design Details

- **PIN generation:** `PIN = SHA256(username + password + time_interval) mod 1,000,000`, zero-padded to 6 digits — the shared secret (username + password) combined with a synchronized time counter means both sides can independently compute the same PIN without transmitting it directly
- **Password strength validation:** enforced minimum length (8 characters) and requires a mix of letters, digits, and symbols at registration
- **Grace window:** authentication checks the PIN against both the current and immediately preceding time interval, accounting for natural delay between PIN generation and submission

## ▶️ Usage

**1. Register a new user:**
```bash
python connect.py Alice new
```

**2. Run the device to generate PINs:**
```bash
python device.py Alice My$ecure123
```

**3. Authenticate:**
```bash
python connect.py Alice My$ecure123 <pin>
```

## 🛠️ Files

- **`device.py`** — simulated hardware token, generates a new PIN every 15 seconds
- **`connect.py`** — user registration and authentication logic
- **`Passwords.txt`** — generated on first registration, stores registered credentials

## 📊 Results

Successfully implemented a working two-factor authentication flow: registration enforces password strength requirements, the simulated device independently generates time-synchronized PINs, and the authentication service correctly validates credentials plus a matching PIN within the tolerance window — rejecting invalid or expired PINs as expected.

## 🎯 Relevance to Blue Team / Security

Understanding how TOTP-style 2FA actually works under the hood — time-synchronized shared secrets, grace windows, and why storing this correctly (or incorrectly) matters — is directly relevant to evaluating authentication system security in a defensive context, including recognizing 2FA bypass techniques (e.g. time-window abuse, replay attacks) and understanding the security trade-offs of different 2FA implementations when reviewing an organization's authentication architecture.

## ⚠️ Note

As per assignment instructions, passwords are stored in plain text in `Passwords.txt` for demonstration purposes — this is **not** a secure practice for real systems (passwords should always be hashed and salted, e.g. with bcrypt or Argon2). This implementation is a simplified educational exercise focused on the TOTP mechanism, not a production-ready authentication system.
