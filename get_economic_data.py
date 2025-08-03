"""
This script fetches key economic indicators from the Federal Reserve Economic Data (FRED) API
and saves the data to a CSV file. It is intended to be run once to gather the initial dataset.
"""

import requests
import pandas as pd
import logging

# --- Configuration ---

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# IMPORTANT: Do not commit your real API key to a public GitHub repository.
# For a professional project, you would use an environment variable.
# For this project, just remember to keep your key private.
FRED_API_KEY = 'YOUR_API_KEY_HERE'

# Define the economic indicators we want using their official FRED Series IDs.
INDICATOR_SERIES_IDS = {
    '10_Year_Treasury_Yield': 'DGS10',
    'Fed_Funds_Rate': 'DFF',
    'Consumer_Price_Index': 'CPIAUCSL' # A common proxy for inflation
}

# --- Main Function ---

def fetch_and_save_economic_data():
    """
    Connects to the FRED API, downloads data for specified indicators,
    and saves the combined data to 'economic_data.csv'.
    """
    base_url = "https://api.stlouisfed.org/fred/series/observations"
    all_series_data = []

    for name, series_id in INDICATOR_SERIES_IDS.items():
        logging.info(f"Fetching data for {name} ({series_id})...")

        params = {
            'series_id': series_id,
            'api_key': FRED_API_KEY,
            'file_type': 'json',
            'observation_start': '2020-01-01',
            'observation_end': '2025-07-30' # Use a fixed end date for reproducibility
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            data = response.json()

            df = pd.DataFrame(data['observations'])
            df = df[['date', 'value']]
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
            df.rename(columns={'value': name}, inplace=True)
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            all_series_data.append(df)

        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed for {name}: {e}")
            return
        except KeyError:
            logging.error(f"Unexpected JSON structure for {name}. It might be empty.")
            continue

    if not all_series_data:
        logging.error("No data was fetched. Aborting file save.")
        return

    # Combine all the individual dataframes into one
    economic_df = pd.concat(all_series_data, axis=1)

    # Forward-fill missing values (e.g., for weekends/holidays)
    economic_df.ffill(inplace=True)

    # Save the raw data to a CSV file in the correct dbt seeds directory
    economic_df.to_csv('financial_models/seeds/economic_data.csv')
    
    logging.info("Successfully downloaded economic data!")
    logging.info("Data saved to financial_models/seeds/economic_data.csv")
    print("\nHere's a preview of the data:")
    print(economic_df.head())

# --- Execution Block ---

if __name__ == "__main__":
    fetch_and_save_economic_data()