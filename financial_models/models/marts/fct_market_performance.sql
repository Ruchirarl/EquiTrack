-- This is the core data model for the project. It joins stock performance with economic indicators
-- and calculates a rich set of metrics for analysis.

-- CTE 1: Import our clean, foundational data from the staging layer.
with stock_prices as (

    select * from {{ ref('stg_stock_prices') }}

),

economic_data as (

    select * from {{ ref('stg_economic_data') }}

),

-- CTE 2: Calculate foundational financial metrics using our custom macros.
price_with_metrics as (

    select
        price_date,
        ticker,
        close_price,

        {{ calculate_returns('close_price') }} as daily_return,
        {{ calculate_moving_average('close_price', 50) }} as fifty_day_moving_avg,
        {{ calculate_moving_average('close_price', 200) }} as two_hundred_day_moving_avg
        
    from stock_prices

),

-- CTE 3: Add rolling volatility, which depends on the daily_return calculated above.
final_metrics as (

    select
        *,
        {{ calculate_volatility('daily_return', 30) }} as thirty_day_volatility
    from price_with_metrics

),

-- CTE 4: Create a simple daily market index to compare each stock's performance against.
market_index as (

    select
        price_date,
        avg(daily_return) as market_daily_return
    from final_metrics
    group by 1

),

-- CTE 5: Join all data sources together and add final business logic.
final as (

    select
        p.price_date,
        p.ticker,
        -- Assign a sector to each stock for easier grouping
        case
            when p.ticker in ('AAPL', 'MSFT', 'NVDA') then 'Technology'
            when p.ticker in ('JNJ', 'PFE', 'LLY') then 'Healthcare'
            when p.ticker in ('JPM', 'GS', 'BAC') then 'Financials'
        end as sector,
        p.close_price,
        p.daily_return,
        p.fifty_day_moving_avg,
        p.two_hundred_day_moving_avg,
        p.thirty_day_volatility,
        m.market_daily_return,
        -- Calculate how much a stock outperformed or underperformed the market
        (p.daily_return - m.market_daily_return) as market_outperformance,
        -- Join in the economic data for the day
        e.ten_year_treasury_yield,
        e.fed_funds_rate,
        e.cpi,
        -- Classify the economic environment for the day
        case
            when e.ten_year_treasury_yield < e.fed_funds_rate then 'Inverted Yield Curve'
            when e.fed_funds_rate > 3.0 then 'High Interest Rate Environment'
            when e.fed_funds_rate < 1.0 then 'Low Interest Rate Environment'
            else 'Normal Interest Rate Environment'
        end as macro_regime

    from final_metrics as p
    left join economic_data as e on p.price_date = e.price_date
    left join market_index as m on p.price_date = m.price_date

)

-- Final selection of all columns from our assembled table.
select * from final