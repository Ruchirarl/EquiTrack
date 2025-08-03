-- This dimension model calculates the correlation between the daily returns of each pair of market sectors.
-- The grain of this table is one row per unique pair of sectors.

-- CTE 1: Calculate the average daily return for each sector.
with sector_performance as (

    select
        price_date,
        sector,
        avg(daily_return) as sector_daily_return
    from {{ ref('fct_market_performance') }}
    where sector is not null
    group by 
        price_date,
        sector

)

-- Final step: Join the sector performance table to itself to create pairs and calculate correlation.
select
    s1.sector as sector_a,
    s2.sector as sector_b,
    -- Calculate the correlation between the two sectors' daily returns over the entire period.
    corr(s1.sector_daily_return, s2.sector_daily_return) as correlation
from sector_performance as s1
-- Join the table to itself on the date to compare the daily returns side-by-side.
inner join sector_performance as s2 on s1.price_date = s2.price_date
-- This clever condition ensures we only get unique pairs (e.g., Tech-Finance)
-- and prevents a sector from being correlated with itself.
where s1.sector < s2.sector
group by 1, 2
order by 3 desc