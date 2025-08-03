-- This staging model transforms the raw stock price data from a wide format to a long format.
-- This "unpivot" is a crucial step to make the data usable for analysis.

with source as (

    -- Import the raw data from the seed file
    select * from {{ ref('stock_prices') }}

)

-- Unpivot the data by creating a separate select statement for each ticker
-- and stacking them on top of each other using UNION ALL.
select
    "Date" as price_date,
    'AAPL' as ticker,
    "AAPL" as close_price
from source
union all
select
    "Date" as price_date,
    'MSFT' as ticker,
    "MSFT" as close_price
from source
union all
select
    "Date" as price_date,
    'NVDA' as ticker,
    "NVDA" as close_price
from source
union all
select
    "Date" as price_date,
    'JNJ' as ticker,
    "JNJ" as close_price
from source
union all
select
    "Date" as price_date,
    'PFE' as ticker,
    "PFE" as close_price
from source
union all
select
    "Date" as price_date,
    'LLY' as ticker,
    "LLY" as close_price
from source
union all
select
    "Date" as price_date,
    'JPM' as ticker,
    "JPM" as close_price
from source
union all
select
    "Date" as price_date,
    'GS' as ticker,
    "GS" as close_price
from source
union all
select
    "Date" as price_date,
    'BAC' as ticker,
    "BAC" as close_price
from source