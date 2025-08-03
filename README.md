# EquiTrack - A Quantitative Platform for Strategic Portfolio Analysis
<p align="center">
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white" alt="dbt" />
<img src="https://img.shields.io/badge/DuckDB-FFF000?style=for-the-badge&logo=duckdb&logoColor=black" alt="DuckDB" />
<img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="scikit-learn" />
<img src="https://img.shields.io/badge/Tableau-E97627?style=for-the-badge&logo=tableau&logoColor=white" alt="Tableau" />
</p>

This project is a **comprehensive**, **end-to-end data platform** that ingests financial market data, models it using an analytics engineering workflow, and trains predictive machine learning models. The final output is a professional-grade strategic dashboard built in Tableau that allows for dynamic portfolio analysis.

## Real-World Relevance
In the world of **finance and consulting**, decisions worth billions are made by analyzing the very data this project handles. Asset management firms, investment banks, and strategic consultants constantly build systems to understand market dynamics, assess portfolio risk, and identify opportunities based on economic trends. This project mirrors a real-world professional workflow, demonstrating the ability to not only process and analyze complex financial data but also to build the robust, automated infrastructure required to deliver timely and trustworthy insights for high-stakes decision-making.

## Project Architecture
This diagram visually represents the complete workflow of the EquiTrack platform, illustrating the flow of data from external sources through the transformation pipeline, and finally to the analytical and predictive outputs.
<p align="center">
<img width="809" height="811" alt="image" src="https://github.com/user-attachments/assets/2b9262e2-9554-4a81-bfb7-d48ab90d4ea5" />
</p>

---

## Core Features
- **Automated Data Pipeline:** A Python-based scheduler (pipeline.py) automates the entire workflow, from data ingestion to model transformation and testing.

- **Advanced Data Transformation with dbt:** Uses dbt to build a robust, multi-layered data model, calculating complex financial metrics like moving averages, volatility, Beta, Sharpe Ratio, and sector performance.

- **Predictive Modeling:** Trains machine learning models (predictive_model.py) to forecast next-day stock returns based on historical and economic data, using TimeSeriesSplit for robust validation.

- **Professional Tooling:** Utilizes a modern data stack and analytics engineering best practices, including version control with Git.

## Financial Glossary
For a complete guide to all the financial metrics and stock tickers used in this project, please see the detailed glossary file included in the repository:
[Download the Financial Glossary](EquiTrack/EquiTrack Glossary.xlsx)

## Project Structure
The project is organized into two main sections: the root directory for Python scripts and the financial_models directory for the dbt project.
```
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
```
--- 
## How to Run This Project
**1. Clone the repository:**
```
git clone <your-repo-url>
```
**2. Set up the Python environment:**
```
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```
**3. Run the initial data download (only needs to be done once):**
> [!NOTE]
> You will need a free API key from the FRED website for the economic data script.
```
python get_stock_data.py
python get_economic_data.py
```
**4. Build the dbt project (models and tests):**
```
cd financial_models
dbt deps  # Install dbt packages
dbt build # Seed, run, and test all models
cd ..
```
**5. Train the machine learning models:**
```
python predictive_model.py
```
**6. Connect Tableau or any other tool to the financial_models/dev.duckdb file to create the final dashboard.**

## Tableau Dashboard
### [Explore the Interactive Dashboard on Tableau Public](https://public.tableau.com/views/EquiTrack-StrategicPortfolioAnalyzer/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)
<p align="center">
<img width="1598" height="894" alt="image" src="https://github.com/user-attachments/assets/dde439ee-867d-4a66-b36b-7880ff420ff8" />
</p>


The dashboard is composed of several key analytical charts, each designed to answer a specific question:
| Chart  | What it Shows |
| ------------- | ------------- |
| KPI Cards  | Provides an at-a-glance summary of the portfolio's key risk and return metrics (Sharpe, Beta, Volatility, Total Return).  |
| Portfolio vs. Market Cumulative Growth  | Compares the growth of selected stocks (the portfolio) against the average growth of the entire market over time, showing if the strategy is winning or losing.  |
| Daily Price vs. 200-Day Moving Average  | Shows the daily price of each selected stock against its long-term (200-day) moving average to identify trends.  |
| Portfolio Composition by Ticker  | A donut chart showing the percentage breakdown of the selected stocks in the portfolio by ticker.  |
| Portfolio Composition by Sector  | A donut chart showing the portfolio's high-level allocation across different sectors (Tech, Healthcare, Financials).  |
| Sector Performance by Economic Regime  | A stacked bar chart showing the average performance of each sector in different economic environments.  |
| Economic Sensitivity Analysis  | A lollipop chart that shows how strongly each stock's performance is correlated to key economic indicators.  |
| Monthly Sector Outperformance vs. Market  | A diverging bar chart that shows which sectors beat (positive) or lagged (negative) the market each month.  |
| 30-Day Volatility Timeline  | An area chart that shows how the overall riskiness of the selected portfolio has changed over time.  |

---
