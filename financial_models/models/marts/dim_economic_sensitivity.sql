-- This dimension model summarizes each stock's sensitivity to key economic indicators.
-- The grain of this table is one row per stock ticker.

select
    ticker,
    sector,

    -- Calculate the correlation between the stock's daily return and the 10-Year Treasury Yield.
    -- A positive value means the stock tends to perform well when yields rise.
    -- A negative value means it tends to perform poorly when yields rise.
    corr(daily_return, ten_year_treasury_yield) as correlation_to_treasury,

    -- Calculate the correlation between the stock's daily return and the Fed Funds Rate.
    corr(daily_return, fed_funds_rate) as correlation_to_fed_rate,

    -- This classifies each stock based on which economic factor it has the strongest relationship with (either positive or negative).
    case
        when abs(corr(daily_return, ten_year_treasury_yield)) > abs(corr(daily_return, fed_funds_rate))
            then 'More Sensitive to Treasury Yields'
        else 'More Sensitive to Fed Policy'
    end as primary_economic_driver

from {{ ref('fct_market_performance') }}
-- We must filter out nulls for the correlation function to work correctly.
where 
    daily_return is not null
    and ten_year_treasury_yield is not null
    and fed_funds_rate is not null
group by
    ticker,
    sector