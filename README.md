# 📈 Stock Market Report Generator  

This project fetches stock market data, generates a PDF report, and sends it via email using Gmail SMTP.  

## 📂 Project Structure  

```
📁 stock_report_project/
│-- 📄 main.py           # Main script to fetch data, generate PDF, and send email  
│-- 📄 generate_data.py  # Handles stock data fetching and PDF generation  
│-- 📄 email_sender.py   # Handles email sending via SMTP  
│-- 📄 .env              # Stores email credentials (not to be shared)  
│-- 📁 reports/          # Stores generated PDF reports  
│-- 📄 README.md         # Project documentation  
```

## 🛠️ Installation & Setup  

1. Clone the repository:  
   ```sh
   git clone https://github.com/JackMwisa/Python-Automation-Practice.git
   cd stock-report
   ```

2. Install required dependencies:  
   ```sh
   pip install -r requirements.txt
   ```

3. Create a `.env` file and add your email credentials:  
   ```
   GMAIL_EMAIL=your-email@gmail.com  
   GMAIL_PASSWORD=your-app-password  
   ```

   **Note:** Enable "Less secure apps" or generate an App Password for Gmail SMTP.

## 🚀 Usage  

Run the main script:  
```sh
python main.py
```

## 📧 Features  

- Fetches stock market data for multiple companies  
- Generates a detailed PDF report  
- Automatically sends the report via email  

## 📜 License  

This project is licensed under the MIT License.  
