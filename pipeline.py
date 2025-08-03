"""
This script orchestrates the entire financial data pipeline.
It loads fresh raw data into the data warehouse and then triggers dbt to transform
that data into the final analytical models. It is designed to be run on a schedule.
"""

import schedule
import time
import subprocess
import duckdb
import logging

# --- Configuration ---
# Set up logging to monitor the pipeline's activity
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
DB_FILE = 'financial_models/dev.duckdb' # Define the path to the DuckDB database

# --- Main Pipeline Class ---
class FinancialPipeline:
    """A class to manage the automated ELT (Extract, Load, Transform) pipeline."""
    
    def __init__(self, api_key):
        self.api_key = api_key
        # Define the names of the raw tables that dbt will source from.
        self.raw_stock_table = 'stock_prices'
        self.raw_economic_table = 'economic_data'

    def load_raw_data(self):
        """
        Loads data from the source CSV files into the DuckDB warehouse.
        In a production system, this step would fetch new data from APIs. For this project,
        it re-loads the CSVs to ensure the database is in sync with the files.
        """
        try:
            logging.info("Loading raw data from CSVs into DuckDB...")
            with duckdb.connect(DB_FILE) as con:
                # This command reads the CSVs from the seeds folder and creates (or replaces) tables in DuckDB.
                # This ensures that every pipeline run starts with the correct raw data.
                con.execute(f"CREATE OR REPLACE TABLE {self.raw_stock_table} AS SELECT * FROM read_csv_auto('financial_models/seeds/{self.raw_stock_table}.csv', header=True)")
                con.execute(f"CREATE OR REPLACE TABLE {self.raw_economic_table} AS SELECT * FROM read_csv_auto('financial_models/seeds/{self.raw_economic_table}.csv', header=True)")
            logging.info("Raw data tables updated successfully in DuckDB.")
        except Exception as e:
            logging.error(f"Error during raw data load: {e}")

    def run_dbt(self):
        """
        Runs the dbt build command to execute all models and tests.
        This transforms the raw data into our final analytical tables.
        """
        try:
            logging.info("Starting dbt build...")
            # 'dbt build' is a convenient command that runs models and tests in the correct order.
            result = subprocess.run(
                ['dbt', 'build'], 
                cwd='financial_models',      # Run the command from within the dbt project folder
                capture_output=True,         # Capture the command's output
                text=True,                   # Decode the output as text
                check=True                   # Raise an error if the command fails
            )
            logging.info("dbt build successful.")
            logging.info(result.stdout)      # Print the output from dbt
        except subprocess.CalledProcessError as e:
            logging.error("dbt build failed.")
            logging.error(e.stderr)          # Print the error output from dbt
        except Exception as e:
            logging.error(f"An unexpected error occurred while running dbt: {e}")

    def run_full_pipeline(self):
        """Runs the entire pipeline in sequence: Load -> Transform -> Test."""
        self.load_raw_data()
        self.run_dbt()

    def start_scheduler(self):
        """Starts the pipeline scheduler to run the job at a defined interval."""
        logging.info("Pipeline scheduler started.")
        
        # Schedule the full pipeline to run once every day at 8:00 AM.
        schedule.every().day.at("08:00").do(self.run_full_pipeline)
        
        # --- For demonstration, let's run it once right now on startup ---
        logging.info("Performing initial run on startup...")
        self.run_full_pipeline()
        logging.info("Initial run complete. Waiting for the next scheduled run...")
        
        while True:
            schedule.run_pending()
            time.sleep(1)

# --- Main Execution Block ---
if __name__ == "__main__":
    # IMPORTANT: Replace with your actual FRED API key
    FRED_API_KEY = '2b86e15ffc99634e5eb571ffe0f888ee'
    
    pipeline = FinancialPipeline(api_key=FRED_API_KEY)
    pipeline.start_scheduler()