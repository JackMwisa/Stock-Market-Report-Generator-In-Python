from generate_data import fetch_stock_data, generate_pdf
from email_sender import send_email

def main():
    tickers = ["GOOGL", "AAPL", "MSFT", "AMZN", "FMC", "TSLA"]
    days = 10
    data_dict = {}

    print("Fetching stock data...")
    for ticker in tickers:
        try:
            stock_data = fetch_stock_data(ticker, days)
            if not stock_data.empty:
                data_dict[ticker] = stock_data
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")

    if data_dict:
        try:
            pdf_file = generate_pdf(data_dict)
            send_email(pdf_file)
        except Exception as e:
            print(f"❌ Error generating/sending report: {e}")
    else:
        print("⚠️ No data available for any tickers")

if __name__ == "__main__":
    main()
