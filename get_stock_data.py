"""
This script fetches historical stock price data from Yahoo Finance for a predefined
list of tickers and saves the data to a CSV file. It is intended to be run once
to gather the initial dataset.
"""

import yfinance as yf
import pandas as pd
import logging

# --- Configuration ---

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Define the companies and their sectors we want to analyze.
# We use major companies as proxies for their respective sectors.
TICKERS = {
    'Technology': ['AAPL', 'MSFT', 'NVDA'],
    'Healthcare': ['JNJ', 'PFE', 'LLY'],
    'Financials': ['JPM', 'GS', 'BAC']
}

# --- Main Function ---

def fetch_and_save_stock_data():
    """
    Downloads historical stock data for the defined tickers and saves the
    adjusted closing prices to 'stock_prices.csv'.
    """
    # Flatten the dictionary of tickers into a single list for the download
    all_tickers = [ticker for sector_tickers in TICKERS.values() for ticker in sector_tickers]

    logging.info(f"Downloading data for: {', '.join(all_tickers)}")

    try:
        # Download historical data from the start of 2020 until today.
        stock_data = yf.download(all_tickers, start="2020-01-01", end="2025-07-30")

        # The 'Close' column contains the adjusted closing price by default in recent yfinance versions.
        close_data = stock_data['Close']

        # Save the raw data to a CSV file in the correct dbt seeds directory
        close_data.to_csv('financial_models/seeds/stock_prices.csv')

        logging.info("Successfully downloaded stock prices!")
        logging.info("Data saved to financial_models/seeds/stock_prices.csv")
        print("\nHere's a preview of the data:")
        print(close_data.head())

    except Exception as e:
        logging.error(f"An error occurred during download: {e}")

# --- Execution Block ---

if __name__ == "__main__":
    fetch_and_save_stock_data()