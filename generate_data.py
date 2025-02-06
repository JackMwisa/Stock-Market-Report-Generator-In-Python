# stock_report.py
import yfinance as yf
from datetime import datetime, timedelta
from fpdf import FPDF


def fetch_stock_data(ticker, days):
    """Get stock data for specified number of days"""
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days)
    
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date)
    
    return data[['Open', 'Close', 'High', 'Low', 'Volume']]

if __name__ == "__main__":
    # Test with Apple stock for 7 days
    print(fetch_stock_data("AAPL", 7).head())