import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def send_email(pdf_filename):
    """Send the PDF report via Gmail."""
    msg = MIMEMultipart()
    msg['From'] = os.getenv("GMAIL_EMAIL")
    msg['To'] = os.getenv("GMAIL_EMAIL")  # Send to yourself or another recipient
    msg['Subject'] = "Daily Stock Market Report"

    # Email body
    body = "Attached is the latest stock market report."
    msg.attach(MIMEText(body, 'plain'))

    # Attach PDF
    with open(pdf_filename, "rb") as f:
        attach = MIMEApplication(f.read(), _subtype="pdf")
        attach.add_header('Content-Disposition', 'attachment', filename=os.path.basename(pdf_filename))
        msg.attach(attach)

    # Gmail SMTP configuration
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(os.getenv("GMAIL_EMAIL"), os.getenv("GMAIL_PASSWORD"))  
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Error sending email: {e}")
