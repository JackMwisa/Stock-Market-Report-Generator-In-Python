import schedule
import time
from generate_data import process_stock_report
from email_sender import send_email

def job():
    """Generate a stock report and send it via email."""
    pdf_filename = process_stock_report()
    if pdf_filename:
        send_email(pdf_filename)
    else:
        print("⚠️ No report generated. Skipping email.")

# Schedule the job to run every 7 days
schedule.every(1).days.do(job)

print("📅 Scheduler started. Running every day.")

while True:
    schedule.run_pending()
    time.sleep(10)  # Check every minute
