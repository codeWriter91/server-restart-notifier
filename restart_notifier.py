import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime  # Import for UTC timestamp

# File to track last uptime
UPTIME_FILE = "/home/ec2-user/server-restart-notifier/last_uptime.txt"

# Email Configuration
EMAIL_SENDER = "aws.xxxx@gmail.com"  # Sender's email address (Gmail)
EMAIL_RECEIVER = "aws.xxxx@gmail.com"  # Recipient's email address
EMAIL_PASSWORD = "udqs xxxx xxxx alat"  # App password for the Gmail account
SMTP_SERVER = "smtp.gmail.com"  # Gmail's SMTP server
SMTP_PORT = 587  # Port for secure SMTP communication

def get_system_uptime():
    """
    Retrieve the system uptime in seconds.

    This function reads from the '/proc/uptime' file, which provides the
    time since the system was last restarted. The first value in the file
    represents the uptime in seconds.
    """
    with open('/proc/uptime', 'r') as f:
        uptime = float(f.readline().split()[0])
    return uptime

def send_notification(subject, body):
    """
    Send an email notification.

    Args:
        subject (str): The subject of the email.
        body (str): The body content of the email.

    This function formats and sends an email using the Gmail SMTP server.
    It also appends the current UTC timestamp to the email body.
    """
    # Get the current UTC timestamp
    utc_timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    body = f"{body}\n\nTimestamp: {utc_timestamp}"
    
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send the email using the SMTP server
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Start TLS encryption
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)  # Log in to Gmail
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())  # Send email
        print(f"Notification sent successfully at {utc_timestamp}.")
    except Exception as e:
        print(f"Failed to send notification: {e}")

def check_for_restart():
    """
    Check if the server has restarted.

    This function compares the current system uptime with the last recorded
    uptime stored in the 'last_uptime.txt' file. If the current uptime is less
    than the last recorded uptime, a restart is detected, and an email is sent.
    """
    # Debugging: Print the current uptime for tracking
    print(f"Current uptime: {get_system_uptime()} seconds")
    
    # Retrieve the current system uptime
    current_uptime = get_system_uptime()
    last_uptime = None

    # Read the last recorded uptime from the file, if it exists
    if os.path.exists(UPTIME_FILE):
        with open(UPTIME_FILE, 'r') as f:
            last_uptime = float(f.read().strip())

    # Check if a restart has occurred
    if last_uptime is None or current_uptime < last_uptime:
        subject = "Server Restart Detected"
        body = f"Server 'prod1' was restarted. Current uptime: {current_uptime} seconds."
        send_notification(subject, body)

    # Update the uptime file with the current uptime
    with open(UPTIME_FILE, 'w') as f:
        f.write(str(current_uptime))

if __name__ == "__main__":
    # Run the script continuously, checking for restarts every 60 seconds
    while True:
        check_for_restart()
        time.sleep(60)  # Pause for 60 seconds before the next check
