import yfinance as yf
from datetime import datetime, timedelta
from fpdf import FPDF

def fetch_stock_data(ticker, days):
    """Fetch stock data for a specified number of days."""
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days)

    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date)

    return data[['Open', 'Close', 'High', 'Low', 'Volume']]

def generate_pdf(data_dict):
    """Generate a simple PDF report for multiple stocks."""
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Stock Market Report", ln=True, align='C')

    # Date and Time of Report
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
        pdf.cell(35, 10, "Date", border=1)
        pdf.cell(30, 10, "Open", border=1)
        pdf.cell(30, 10, "Close", border=1)
        pdf.cell(30, 10, "High", border=1)
        pdf.cell(30, 10, "Low", border=1)
        pdf.cell(35, 10, "Volume", border=1)
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

    # Save PDF with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"reports/Stock_Report_{timestamp}.pdf"
    pdf.output(filename)
    print(f"PDF report saved as {filename}")
    return filename

if __name__ == "__main__":
    tickers = ["AAPL", "GOOGL", "MSFT"]  # Add more ticker symbols if needed
    days = 10
    data_dict = {}

    print("Fetching stock data...")
    for ticker in tickers:
        stock_data = fetch_stock_data(ticker, days)
        if not stock_data.empty:
            data_dict[ticker] = stock_data

    if data_dict:
        print("Generating PDF report...")
        generate_pdf(data_dict)
    else:
        print("No data available for the selected tickers.")