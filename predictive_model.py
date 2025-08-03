"""
This script builds and trains machine learning models to predict next-day stock returns.
It loads the final analytical data model from dbt, engineers features, trains a separate
Gradient Boosting model for each stock, and saves the trained models to disk.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import r2_score
import joblib
import duckdb
import os
import logging

# --- Configuration ---
# Set up logging to monitor the ML training process
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
DB_PATH = 'financial_models/dev.duckdb'
MODELS_DIR = 'trained_models'

# --- Main ML Model Class ---
class FinancialMLModel:
    """A class to manage the machine learning pipeline for financial prediction."""
    
    def __init__(self):
        self.models = {}
        self.feature_importance = {}

    def _load_data(self):
        """Loads the final analytical base table from the DuckDB warehouse."""
        logging.info("Loading data from DuckDB for ML training...")
        with duckdb.connect(DB_PATH, read_only=True) as con:
            df = con.execute("SELECT * FROM fct_market_performance").fetchdf()
        return df

    def prepare_features(self, df):
        """
        Engineers features for the ML models, including lagged variables.
        Args:
            df (pd.DataFrame): The input dataframe from the data warehouse.
        Returns:
            pd.DataFrame: The dataframe with new features and the target variable.
        """
        logging.info("Preparing features for ML models...")
        df = df.sort_values(by=['ticker', 'price_date'])

        # Create lagged features for historical returns using groupby().shift()
        lags = [1, 5, 10]
        for lag in lags:
            df[f'return_lag_{lag}'] = df.groupby('ticker')['daily_return'].shift(lag)
        
        # Define our target variable: we want to predict the *next* day's return
        df['target_return'] = df.groupby('ticker')['daily_return'].shift(-1)
        
        # Drop rows with NA values that were created by our lagging/shifting operations
        df.dropna(inplace=True)
        return df

    def train_model_for_ticker(self, ticker, data):
        """
        Trains a Gradient Boosting Regressor for a single stock ticker.
        Uses TimeSeriesSplit for robust cross-validation suitable for financial data.
        """
        logging.info(f"Starting training for ticker: {ticker}")
        
        ticker_data = data[data['ticker'] == ticker]
        
        feature_columns = [
            'daily_return', 'fifty_day_moving_avg', 'two_hundred_day_moving_avg',
            'thirty_day_volatility', 'ten_year_treasury_yield', 'fed_funds_rate',
            'return_lag_1', 'return_lag_5', 'return_lag_10'
        ]
        
        X = ticker_data[feature_columns]
        y = ticker_data['target_return']
        
        if len(X) < 100: # Ensure we have enough data to train a meaningful model
            logging.warning(f"Insufficient data for {ticker}, skipping training.")
            return

        # TimeSeriesSplit is crucial for time-series data to prevent looking into the future during validation.
        tscv = TimeSeriesSplit(n_splits=5)
        model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
        
        # Perform cross-validation to get a realistic estimate of the model's performance on unseen data.
        scores = []
        for train_index, test_index in tscv.split(X):
            X_train, X_test = X.iloc[train_index], X.iloc[test_index]
            y_train, y_test = y.iloc[train_index], y.iloc[test_index]
            model.fit(X_train, y_train)
            scores.append(r2_score(y_test, model.predict(X_test)))
        
        logging.info(f"Model for {ticker} - Cross-Validation R² Score: {np.mean(scores):.4f}")
        
        # Train the final model on all available data for this ticker
        model.fit(X, y)
        self.models[ticker] = model

    def save_models(self):
        """Saves all trained models to disk using joblib for efficient persistence."""
        if not os.path.exists(MODELS_DIR):
            os.makedirs(MODELS_DIR)
        
        for ticker, model in self.models.items():
            joblib.dump(model, os.path.join(MODELS_DIR, f'{ticker}_model.pkl'))
        
        logging.info(f"All trained models have been saved to the '{MODELS_DIR}/' directory.")

    def run_training_pipeline(self):
        """Executes the full pipeline: Load -> Prepare Features -> Train -> Save."""
        data = self._load_data()
        prepared_data = self.prepare_features(data)
        
        for ticker in prepared_data['ticker'].unique():
            self.train_model_for_ticker(ticker, prepared_data)
            
        self.save_models()

# --- Main Execution Block ---
if __name__ == "__main__":
    ml_pipeline = FinancialMLModel()
    ml_pipeline.run_training_pipeline()