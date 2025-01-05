import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# File to track last uptime
UPTIME_FILE = "/home/ec2-user/server-restart-notifier/last_uptime.txt"

# Email Configuration
EMAIL_SENDER = "aws.xxxx@gmail.com"  
EMAIL_RECEIVER = "aws.xxxx@gmail.com"  
EMAIL_PASSWORD = "udqs xxxx xxxx alat"  
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def get_system_uptime():
    """Retrieve the system uptime in seconds."""
    with open('/proc/uptime', 'r') as f:
        uptime = float(f.readline().split()[0])
    return uptime

def send_notification(subject, body):
    """Send an email notification."""
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print("Notification sent successfully.")
    except Exception as e:
        print(f"Failed to send notification: {e}")

def check_for_restart():
    print(f"Current uptime: {get_system_uptime()} seconds")
    """Check if the server has restarted."""
    current_uptime = get_system_uptime()
    last_uptime = None

    
    if os.path.exists(UPTIME_FILE):
        with open(UPTIME_FILE, 'r') as f:
            last_uptime = float(f.read().strip())

    # If last uptime is None or current uptime is less than last uptime, a restart occurred
    if last_uptime is None or current_uptime < last_uptime:
        subject = "Server Restart Detected"
        body = f"Server 'prod1' was restarted. Current uptime: {current_uptime} seconds."
        send_notification(subject, body)

    # Update the uptime file
    with open(UPTIME_FILE, 'w') as f:
        f.write(str(current_uptime))

if __name__ == "__main__":
    while True:
        check_for_restart()
        time.sleep(60)  # Check every 60 seconds
