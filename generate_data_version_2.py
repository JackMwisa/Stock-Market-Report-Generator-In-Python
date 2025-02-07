import os
import yfinance as yf
import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from fpdf import FPDF
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def fetch_stock_data(ticker, days):
    """Fetch stock data for a specified number of days."""
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days)

    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date)

    return data[['Open', 'Close', 'High', 'Low', 'Volume']]

def generate_pdf(data_dict):
    """Generate a PDF report for multiple stocks."""
    # Create reports directory if it doesn't exist
    os.makedirs("reports", exist_ok=True)
    
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Stock Market Report", ln=True, align='C')

    # Date and Time
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, f"Generated on: {current_time}", ln=True, align='C')
    pdf.ln(10)

    # Generate tables for each ticker
    for ticker, data in data_dict.items():
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, f"Stock: {ticker}", ln=True, align='L')
        pdf.ln(5)
        
        # Table Header
        pdf.set_font("Arial", "B", 10)
        headers = ["Date", "Open", "Close", "High", "Low", "Volume"]
        widths = [35, 30, 30, 30, 30, 35]

        for h, w in zip(headers, widths):
            pdf.cell(w, 10, h, border=1)
        pdf.ln()

        # Table Data
        pdf.set_font("Arial", "", 10)
        for index, row in data.iterrows():
            pdf.cell(35, 10, index.strftime('%Y-%m-%d'), border=1)
            pdf.cell(30, 10, f"{row['Open']:.2f}", border=1)
            pdf.cell(30, 10, f"{row['Close']:.2f}", border=1)
            pdf.cell(30, 10, f"{row['High']:.2f}", border=1)
            pdf.cell(30, 10, f"{row['Low']:.2f}", border=1)
            pdf.cell(35, 10, f"{int(row['Volume'])}", border=1)
            pdf.ln()

        pdf.ln(10)

    # Save PDF
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"reports/Stock_Report_{timestamp}.pdf"
    pdf.output(filename)
    print(f"PDF report saved as {filename}")
    return filename

def send_email(pdf_filename):
    """Send the PDF report via email to ProtonMail."""
    # Create message
    msg = MIMEMultipart()
    msg['From'] = os.getenv("PROTONMAIL_EMAIL")
    msg['To'] = os.getenv("PROTONMAIL_EMAIL")  # Send to yourself
    msg['Subject'] = "Daily Stock Market Report"

    # Email body
    body = "Attached is the latest stock market report."
    msg.attach(MIMEText(body, 'plain'))

    # Attach PDF
    with open(pdf_filename, "rb") as f:
        attach = MIMEApplication(f.read(), _subtype="pdf")
        attach.add_header('Content-Disposition', 'attachment', 
                        filename=os.path.basename(pdf_filename))
        msg.attach(attach)

    # ProtonMail SMTP configuration
    try:
        server = smtplib.SMTP("mail.protonmail.ch", 587)
        server.starttls()
        server.login(os.getenv("PROTONMAIL_EMAIL"), os.getenv("PROTONMAIL_PASSWORD"))
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

if __name__ == "__main__":
    # Configuration
    tickers = ["GOOGL", "AAPL", "MSFT", "AMZN", "FMC", "TSLA"]
    days = 10
    data_dict = {}

    # Fetch data
    print("Fetching stock data...")
    for ticker in tickers:
        try:
            stock_data = fetch_stock_data(ticker, days)
            if not stock_data.empty:
                data_dict[ticker] = stock_data
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")

    if data_dict:
        # Generate PDF
        try:
            pdf_file = generate_pdf(data_dict)
            # Send email
            send_email(pdf_file)
        except Exception as e:
            print(f"❌ Error generating/sending report: {e}")
    else:
        print("⚠️ No data available for any tickers")