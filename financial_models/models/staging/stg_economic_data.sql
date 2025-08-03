-- This staging model cleans up the raw economic data.
-- It renames columns to be more consistent and SQL-friendly.

select
    date as price_date,
    "10_Year_Treasury_Yield" as ten_year_treasury_yield,
    "Fed_Funds_Rate" as fed_funds_rate,
    "Consumer_Price_Index" as cpi
from {{ ref('economic_data') }}