cat <<EOT > README.md
# Server Restart Notifier

A Python script to monitor server uptime and detect restarts. This script is ideal for ensuring server availability and receiving email notifications whenever a restart is detected.

## Features
- Monitors server uptime using \`/proc/uptime\`.
- Detects restarts by comparing the current uptime with the last recorded uptime.
- Sends email notifications with a UTC timestamp when a restart is detected.
- Designed to run continuously using a Systemd service or a session manager.

---

## Prerequisites
1. **AWS EC2 Instance or Linux Server**:
   - The script is designed to run on any Linux-based server that supports \`/proc/uptime\`.

2. **Python 3.6 or Later**:
   - Ensure Python is installed on the server.
   - Install \`secure-smtplib\` if not already installed:
     \`\`\`bash
     pip install secure-smtplib
     \`\`\`

3. **Gmail SMTP Account**:
   - A Gmail account is required to send notifications. Follow the setup instructions below.

---

## Gmail Setup Instructions
To use Gmail for sending email notifications:
1. **Enable 2-Step Verification**:
   - Log in to your Gmail account.
   - Go to [Google Account Security Settings](https://myaccount.google.com/security).
   - Enable **2-Step Verification** under "Signing in to Google."

2. **Generate an App Password**:
   - After enabling 2-Step Verification, navigate to **App Passwords**.
   - Create a new app password:
     - Select "Mail" as the app.
     - Select "Other (Custom)" as the device and name it (e.g., \`Server Notifier\`).
   - Copy the generated 16-character password and save it securely.

3. **Update Script with Gmail Details**:
   - Replace the following placeholders in the script with your Gmail details:
     - \`EMAIL_SENDER\`: Your Gmail address (e.g., \`your_email@gmail.com\`).
     - \`EMAIL_RECEIVER\`: The recipient email address (can be the same as the sender for testing).
     - \`EMAIL_PASSWORD\`: The app password generated above.

---

## Installation and Usage
1. **Clone the Repository**:
   \`\`\`bash
   git clone https://github.com/codeWriter91/server-restart-notifier.git
   cd server-restart-notifier
   \`\`\`

2. **Update the Configuration**:
   - Open \`restart_notifier.py\` and update the email settings (\`EMAIL_SENDER\`, \`EMAIL_RECEIVER\`, \`EMAIL_PASSWORD\`).

3. **Run the Script**:
   \`\`\`bash
   python3 restart_notifier.py
   \`\`\`

4. **Keep the Script Running**:
    Configure the script as a **Systemd service**:
     - Create a service file:
       \`\`\`bash
       sudo nano /etc/systemd/system/restart-notifier.service
       \`\`\`
       Add the following content:
       \`\`\`ini
       [Unit]
       Description=Server Restart Notifier
       After=network.target

       [Service]
       ExecStart=/usr/bin/python3 /home/ec2-user/server-restart-notifier/restart_notifier.py
       Restart=always
       User=ec2-user

       [Install]
       WantedBy=multi-user.target
       \`\`\`
     - Reload Systemd and start the service:
       \`\`\`bash
       sudo systemctl daemon-reload
       sudo systemctl enable restart-notifier.service
       sudo systemctl start restart-notifier.service
       \`\`\`

---

## Example Email Notification
Sample email sent upon detecting a server restart:
\`\`\`
Subject: Server Restart Detected
Body:
Server 'prod1' was restarted. Current uptime: 123 seconds.

Timestamp: 2025-01-05 18:25:00 UTC
\`\`\`

---

## Notes
- **Sensitive Information**: Do not store passwords or app credentials directly in the code for production use. Use environment variables or secure secrets management tools.
- **Testing Notifications**: To test notifications, delete the \`last_uptime.txt\` file and restart the script:
  \`\`\`bash
  rm /home/ec2-user/server-restart-notifier/last_uptime.txt
  python3 restart_notifier.py
  \`\`\`

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
EOT
