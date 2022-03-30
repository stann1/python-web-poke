# Import smtplib for the actual sending function
import os
import smtplib
from email.mime.text import MIMEText
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = 'test@holler.solutions'

def send_mail_smpt(recipient_address, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_address

    # Send the message via our own SMTP server.
    try:
        s = smtplib.SMTP(os.getenv('SMTP_SERVER'))
        s.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASS'))
        s.send_message(msg)
        s.quit()
        print("Mail sent.")
    except Exception as e:
        print(e)

def send_mail_sendgrid(recipient_addresses, subject, body):
    message = Mail(
        from_email = SENDER_EMAIL,
        to_emails = recipient_addresses,
        subject = subject,
        html_content = body
    )
    
    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(f"Sendgrid mail success: {response.status_code}")
    except Exception as e:
        print(e)
