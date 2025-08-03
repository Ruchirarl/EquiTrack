Equitrack - A Quantitative Platform for Strategic Portfolio Analysis
<p align="center">
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white" alt="dbt" />
<img src="https://img.shields.io/badge/DuckDB-FFF000?style=for-the-badge&logo=duckdb&logoColor=black" alt="DuckDB" />
<img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="scikit-learn" />
<img src="https://img.shields.io/badge/Tableau-E97627?style=for-the-badge&logo=tableau&logoColor=white" alt="Tableau" />
</p>

📜 Overview
Equitrack is a comprehensive, end-to-end data platform that ingests financial market data, models it using an analytics engineering workflow, applies data quality testing, and trains predictive machine learning models. The final output is a professional-grade strategic dashboard built in Tableau that allows for dynamic portfolio analysis.

This project mirrors a real-world professional workflow in finance and consulting, demonstrating the ability to build robust, automated infrastructure to deliver timely and trustworthy insights for high-stakes decision-making.

✨ Core Features
Automated Data Pipeline: A Python-based scheduler (pipeline.py) automates the entire workflow, from data ingestion to model transformation and testing.

Advanced Data Transformation with dbt: Uses dbt to build a robust, multi-layered data model, calculating complex financial metrics like moving averages, volatility, Beta, Sharpe Ratio, and sector performance.

Data Quality Assurance: Implements a comprehensive testing suite with dbt to ensure the reliability and accuracy of the final data, using both generic and custom tests.

Predictive Modeling: Trains machine learning models (predictive_model.py) to forecast next-day stock returns based on historical and economic data, using TimeSeriesSplit for robust validation.

Professional Tooling: Utilizes a modern data stack and analytics engineering best practices, including version control with Git.

🏗️ Project Architecture
The diagram below illustrates the flow of data from external sources through the transformation and testing pipeline to the final analytical and predictive outputs.

Code snippet

graph TD
    subgraph "1. Data Ingestion (Python)"
        A[External API: yfinance] --> B(get_stock_data.py)
        C[External API: FRED] --> D(get_economic_data.py)
    end

    subgraph "2. Raw Data Storage (CSV Seeds)"
        B --> E[stock_prices.csv]
        D --> F[economic_data.csv]
    end

    subgraph "3. Analytics Engineering (dbt & DuckDB)"
        E -- dbt seed --> G((DuckDB Warehouse))
        F -- dbt seed --> G
        G -- dbt run --> H{Final Analytical Models}
        H -- dbt test --> I[Data Quality Tests Passed]
    end

    subgraph "4. Outputs & Analysis"
        I --> J(predictive_model.py)
        J --> K[Trained ML Models (.pkl)]
        I --> L[Tableau Dashboard]
    end

    subgraph "5. Orchestration (Automation)"
        M(pipeline.py)
        M -.-> B
        M -.-> D
        M -.-> G
        M -.-> H
        M -.-> I
    end

    style A fill:#FFC300,stroke:#333,stroke-width:2px
    style C fill:#FFC3C7,stroke:#333,stroke-width:2px
    style L fill:#DAF7A6,stroke:#333,stroke-width:2px
    style K fill:#DAF7A6,stroke:#333,stroke-width:2px
    style M fill:#FF5733,stroke:#333,stroke-width:2px
🧮 Financial Metrics
This project calculates dozens of key financial indicators. For a complete guide to all the financial metrics and stock tickers used, please see the detailed glossary file included in the repository.

Download the Financial Glossary (Excel File)

📁 Project Structure
The project is organized into two main sections: Python scripts in the root directory and the dbt project within the financial_models directory.

.
├── financial_models/
│   ├── macros/
│   │   └── financial_metrics.sql
│   ├── models/
│   │   ├── marts/
│   │   │   ├── dim_economic_sensitivity.sql
│   │   │   ├── dim_risk_summary.sql
│   │   │   ├── dim_sector_correlations.sql
│   │   │   ├── fct_market_performance.sql
│   │   │   ├── fct_sector_daily.sql
│   │   │   └── marts.yml
│   │   └── staging/
│   │       ├── stg_economic_data.sql
│   │       └── stg_stock_prices.sql
│   ├── seeds/
│   │   ├── economic_data.csv
│   │   └── stock_prices.csv
│   ├── tests/
│   │   └── assert_unreasonable_daily_returns.sql
│   ├── dbt_project.yml
│   └── packages.yml
├── trained_models/
│   └── (Saved .pkl models appear here)
├── .gitignore
├── get_economic_data.py
├── get_stock_data.py
├── pipeline.py
├── predictive_model.py
├── README.md
└── requirements.txt
🚀 How to Run This Project
Prerequisites
Python 3.8+

A free API key from the FRED website for economic data.

Tableau Desktop or Tableau Public to view the dashboard.

1. Clone the Repository
Bash

git clone <your-repo-url>
cd <repository-name>
2. Set Up the Python Environment
Bash

# Create a virtual environment
python -m venv venv

# Activate it (macOS/Linux)
source venv/bin/activate

# Or activate it (Windows)
# .\venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
3. Run Initial Data Download
Note: This only needs to be done once. You will be prompted to enter your FRED API key for the economic data script.

Bash

python get_stock_data.py
python get_economic_data.py
4. Build the dbt Project
This command will seed the raw data into DuckDB, run all transformations, and execute data quality tests.

Bash

# Navigate to the dbt project directory
cd financial_models

# Install dbt packages
dbt deps

# Build the project
dbt build

# Return to the root directory
cd ..
5. Train the Machine Learning Models
Bash

python predictive_model.py
6. Visualize in Tableau
Connect Tableau to the dev.duckdb file located in the financial_models/ directory to view the final analytical models and build your dashboard.

📊 Dashboard Showcase
(Add a screenshot of your final Tableau dashboard here)

[Link to Live Dashboard on Tableau Public]

Dashboard Chart Explanations
The dashboard is composed of several key analytical charts, each designed to answer a specific business question.

Chart	What it Shows
KPI Cards	Provides an at-a-glance summary of the portfolio's key risk and return metrics (Sharpe, Beta, Volatility, Total Return).
Price vs. Trend	Shows the daily price of each selected stock against its long-term (200-day) moving average to identify trends.
Risk & Return Profile	A scatter plot that classifies each stock into one of four quadrants based on its long-term risk and return.
Portfolio Composition	A donut chart showing the percentage breakdown of the selected stocks in the portfolio by ticker.
Sector Composition	A donut chart showing the portfolio's high-level allocation across different sectors (Tech, Healthcare, Financials).
Economic Regime	A stacked bar chart showing the average performance of each sector in different economic environments.
Economic Sensitivity	A lollipop chart that shows how strongly each stock's performance is correlated to key economic indicators.
Sector Outperformance	A diverging bar chart that shows which sectors beat (positive) or lagged (negative) the market each month.
Volatility Timeline	An area chart that shows how the overall riskiness of the selected portfolio has changed over time.
