# Cookie Stealer 

## How to Run

1. Ensure Python 3.12+ and Flask are installed.
   pip install flask

2. Start the Flask receiver:
   python safe_receiver.py

3. Open DVWA in your browser (Meta2 IP) from Kali.

4. In DVWA:
   - Set security level to "medium"
   - Go to "XSS (Reflected)"
   - Paste the contents of payload.txt into the input field and submit. (REMMEBER TO CHANGE THE IP OF YOUR KALI, MINE IS 10.0.2.15 IN GIVEN SCRIPT)

5. Check cookies.txt in the same directory as safe_receiver.py.
   It will contain timestamped cookies from the victim.

## Files
- safe_receiver.py  --> Python Flask server to receive stolen cookies
- payload.txt       --> JavaScript XSS injection payload
- cookies.txt       --> Output log file containing stolen cookies


***** I also provided you with some screenshots of my codes proving that runs perfectly *****
-dvwa.png <-- showing the script in injected
-safe_receiver.png  <-- showing that my python code is running
-cookies.png <---- showing the cookies are saved in the cookies.txt file after injection of the script