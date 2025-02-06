import yfinance as yf
from datetime import datetime, timedelta
from fpdf import FPDF
import os

# Report Directory
REPORTS_DIR = "reports"

def fetch_stock_data(ticker, days=10):
    """Fetch stock data for a given number of days."""
    try:
        end_date = datetime.today()
        start_date = end_date - timedelta(days=days)

        stock = yf.Ticker(ticker)
        data = stock.history(start=start_date, end=end_date)

        if data.empty:
            print(f"⚠️ No data found for {ticker}")
            return None

        return data[['Open', 'Close', 'High', 'Low', 'Volume']]
    
    except Exception as e:
        print(f"❌ Error fetching data for {ticker}: {e}")
        return None

def generate_pdf(data_dict):
    """Generate a PDF report for multiple stocks and save it in reports folder."""
    
    # Ensure reports directory exists
    if not os.path.exists(REPORTS_DIR):
        print(f"📁 Creating reports directory: {REPORTS_DIR}")
        os.makedirs(REPORTS_DIR, exist_ok=True)

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

        pdf.ln(10)  # Space between stocks

    # Save PDF
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(REPORTS_DIR, f"Stock_Report_{timestamp}.pdf")

    try:
        pdf.output(filename)
        if os.path.exists(filename):
            print(f"✅ Report successfully saved: {filename}")
        else:
            print(f"❌ Report failed to save: {filename}")
    except Exception as e:
        print(f"❌ Error saving report: {e}")

    return filename

def process_stock_report():
    """Fetch stock data, generate a report, and return the PDF filename."""
    tickers = ["AAPL", "GOOGL", "MSFT"]
    data_dict = {ticker: fetch_stock_data(ticker) for ticker in tickers if fetch_stock_data(ticker) is not None}

    if data_dict:
        return generate_pdf(data_dict)
    
    print("⚠️ No data available for the selected tickers.")
    return None

