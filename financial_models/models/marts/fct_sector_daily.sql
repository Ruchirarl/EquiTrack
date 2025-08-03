-- This fact table calculates the daily performance for each market sector.
-- The grain of this table is one row per sector per day.

-- CTE 1: Aggregate the individual stock returns up to the sector level for each day.
with sector_performance as (

    select
        price_date,
        sector,
        -- Calculate the average daily return for all stocks within the sector for that day.
        avg(daily_return) as sector_daily_return
    from {{ ref('fct_market_performance') }}
    where sector is not null
    group by 
        price_date,
        sector

),

-- CTE 2: Rank the sectors based on their performance each day.
sector_rankings as (

    select
        *,
        -- The rank() window function partitions by date, so the ranking resets every day.
        rank() over (partition by price_date order by sector_daily_return desc) as daily_return_rank
    from sector_performance

)

-- Final selection of all columns from our ranked table.
select * from sector_rankings