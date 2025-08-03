-- This file contains reusable macros for common financial calculations.
-- These macros help keep our main data models clean and maintainable.

{% macro calculate_returns(price_column, partition_by='ticker', order_by='price_date') %}
    {#
        Calculates the daily percentage return for a price column.
        Args:
            price_column (string): The name of the column with the price.
            partition_by (string): The column to partition the window function by (e.g., 'ticker').
            order_by (string): The column to order the window function by (e.g., 'price_date').
        Returns:
            A SQL expression for the daily return.
    #}
    ({{ price_column }} - lag({{ price_column }}, 1) over (
        partition by {{ partition_by }} 
        order by {{ order_by }}
    )) / lag({{ price_column }}, 1) over (
        partition by {{ partition_by }} 
        order by {{ order_by }}
    )
{% endmacro %}


{% macro calculate_moving_average(column_name, window_days, partition_by='ticker', order_by='price_date') %}
    {#
        Calculates the rolling moving average over a specified window.
        Args:
            column_name (string): The name of the column to average.
            window_days (int): The number of days in the rolling window.
            partition_by (string): The column to partition the window function by.
            order_by (string): The column to order the window function by.
        Returns:
            A SQL expression for the moving average.
    #}
    avg({{ column_name }}) over (
        partition by {{ partition_by }} 
        order by {{ order_by }} 
        rows between {{ window_days - 1 }} preceding and current row
    )
{% endmacro %}


{% macro calculate_volatility(return_column, window_days, partition_by='ticker', order_by='price_date') %}
    {#
        Calculates the rolling volatility (standard deviation of returns) over a specified window.
        Args:
            return_column (string): The name of the column with daily returns.
            window_days (int): The number of days in the rolling window.
            partition_by (string): The column to partition the window function by.
            order_by (string): The column to order the window function by.
        Returns:
            A SQL expression for the rolling volatility.
    #}
    stddev({{ return_column }}) over (
        partition by {{ partition_by }} 
        order by {{ order_by }} 
        rows between {{ window_days - 1 }} preceding and current row
    )
{% endmacro %}