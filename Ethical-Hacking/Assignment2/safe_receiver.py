# safe_receiver.py

from flask import Flask, request, redirect, url_for
from datetime import datetime
import html

app = Flask(__name__)
LOGFILE = "cookies.txt"

@app.route("/")
def index():
    return (
        "<h3>Safe Receiver (lab demo)</h3>"
        "<p>Use the /collect endpoint with ?data=... to send a test value.</p>"
    )

@app.route("/collect", methods=["GET"])
def collect():
    """
    Expected usage (demo): /collect?data=some_test_value
    This function will escape the incoming value, timestamp it, and append to LOGFILE.
    """
    raw = request.args.get("data", "")
    # Safely escape to avoid storing raw HTML
    safe_value = html.escape(raw)
    timestamp = datetime.utcnow().isoformat() + "Z"
    entry = f"{timestamp} - received: {safe_value}\n"

    # Append to file (ensure file permissions are correct on your Kali VM)
    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(entry)

    # Redirect back to a benign confirmation page to mimic realistic behavior
    return redirect(url_for("index"))

if __name__ == "__main__":
    # In your lab, run on the VM's internal IP and bind to 0.0.0.0 if you want other VMs to reach it
    # Example: app.run(host="0.0.0.0", port=8000, debug=False)
    app.run(host="0.0.0.0", port=8000, debug=False)
