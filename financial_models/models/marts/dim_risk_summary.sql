-- This dimension model summarizes the risk and return profile for each stock over the entire historical period.
-- The grain of this table is one row per stock ticker.

-- CTE 1: Import our core fact table.
with stock_performance as (

    select * from {{ ref('fct_market_performance') }}

),

-- CTE 2: A helper to find the very first and very last price for each stock.
-- This is necessary to correctly calculate the total return over the entire period.
price_first_last as (

    select
        ticker,
        -- Get the price from the first day for each stock in our dataset
        first_value(close_price) over (partition by ticker order by price_date asc) as first_price,
        -- Get the price from the most recent day for each stock
        last_value(close_price) over (partition by ticker order by price_date asc rows between unbounded preceding and unbounded following) as last_price,
        price_date -- We need the date to join back
    from stock_performance

),

-- CTE 3: Aggregate the daily data into a final summary for each stock.
final_summary as (

    select
        p.ticker,
        p.sector,

        -- Value at Risk (VaR): A "worst-case scenario" metric.
        -- This tells us the most we could expect to lose on 95% of days.
        percentile_cont(0.05) within group (order by p.daily_return) as value_at_risk_95,

        -- Sharpe Ratio: The key risk-adjusted return metric.
        -- It measures how much return we got for each unit of risk taken. Higher is better.
        (avg(p.daily_return) * 252 - 0.02) / (stddev(p.daily_return) * sqrt(252)) as sharpe_ratio,

        -- Beta: Measures how much a stock's movement correlates with the market's movement.
        -- Beta > 1 suggests more volatility than the market; Beta < 1 suggests less.
        covar_pop(p.daily_return, p.market_daily_return) / var_pop(p.market_daily_return) as beta,

        -- Annualized Volatility: The standard deviation of daily returns, scaled to a yearly figure.
        -- This is a standard measure of a stock's total risk or "jumpiness".
        stddev(p.daily_return) * sqrt(252) as annualized_volatility,

        -- Total Return: The overall percentage gain or loss for the stock over the entire time period.
        max(pfl.last_price / pfl.first_price) - 1 as total_return_pct

    from stock_performance as p
    -- We join our helper CTE here to make the total_return_pct calculation possible
    left join price_first_last as pfl on p.ticker = pfl.ticker and p.price_date = pfl.price_date
    where p.daily_return is not null
    group by 1, 2 -- Group by ticker and sector to create one summary row for each stock

)

select * from final_summary