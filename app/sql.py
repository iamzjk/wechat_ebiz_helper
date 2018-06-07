"""
    SQL Statements
"""


GET_MONTHLY_SALES = """
SELECT
    COUNT(*) AS order_counts,
    SUM(price) AS price,
    SUM(cost) AS cost,
    SUM(shipping) AS shipping,
    (SUM(price) - SUM(cost) - SUM(shipping)) AS gross_profit,
    (SUM(price) - SUM(cost) - SUM(shipping))/SUM(price) AS gross_profit_rate,
    EXTRACT(month from created_time) AS month,
    EXTRACT(year from CURRENT_DATE) AS year
FROM usatocn2013.orders
WHERE client <> '张三'
AND EXTRACT(year from created_time) = EXTRACT(year from CURRENT_DATE)
GROUP BY EXTRACT(month from created_time)
ORDER BY EXTRACT(month from created_time) DESC;
"""

GET_THIS_MONTH_COUNT_TO = """
SELECT
    SUM(price) AS sales,
    (SUM(price) - SUM(cost) - SUM(shipping)) AS gross_profit,
    EXTRACT(year from CURRENT_DATE) AS year,
    EXTRACT(month from CURRENT_DATE) AS month
FROM usatocn2013.orders
WHERE client <> '张三'
AND EXTRACT(year from created_time) = EXTRACT(year from CURRENT_DATE)
AND EXTRACT(month from created_time) = EXTRACT(month from CURRENT_DATE)
GROUP BY EXTRACT(month from created_time);
"""

GET_ALLTIME_CLIENT_RANKING = """
SELECT
    client,
    COUNT(*) AS order_counts,
    SUM(price) AS sales
FROM usatocn2013.orders
WHERE client <> '张三'
GROUP BY client, phone
ORDER BY SUM(price) DESC, COUNT(*) DESC
LIMIT 10;
"""

GET_PERIOD_CLIENT_RANKING = """
SELECT
    client,
    COUNT(*) AS order_counts,
    SUM(price) AS sales
FROM usatocn2013.orders
WHERE client <> '张三'
AND DATE(created_time) >= '{start_date}'
AND DATE(created_time) <= '{end_date}'
GROUP BY client, phone
ORDER BY SUM(price) DESC, COUNT(*) DESC
LIMIT 10;
"""

GET_DAILY_SALES_SUMMARY = """
SELECT
    SUM(price) AS sales,
    (SUM(price) - SUM(cost) - SUM(shipping)) AS gross_profit,
    DATE(created_time) AS date
FROM usatocn2013.orders
WHERE client <> '张三'
AND EXTRACT(month from created_time) = EXTRACT(month from CURRENT_DATE)
AND EXTRACT(year from created_time) = EXTRACT(year from CURRENT_DATE)
GROUP BY DATE(created_time)
ORDER BY DATE(created_time);
"""
