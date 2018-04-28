"""
    SQL Statements
"""


GET_MONTHLY_SALES = """
SELECT
    COUNT(*) AS order_counts,
    SUM(price) AS price,
    SUM(cost) AS cost,
    CAST(SUM(shipping) AS SIGNED) AS shipping,
    (SUM(price) - SUM(cost) - SUM(shipping)) AS gross_profit,
    (SUM(price) - SUM(cost) - SUM(shipping))/SUM(price) AS gross_profit_rate,
    MONTH(created_time) AS month,
    YEAR(NOW()) AS year
FROM usatocn2013.orders
WHERE client <> '张三'
AND YEAR(created_time) = YEAR(NOW())
GROUP BY MONTH(created_time)
ORDER BY MONTH(created_time) DESC;
"""

GET_THIS_MONTH_COUNT_TO = """
SELECT
    SUM(price) AS sales,
    (SUM(price) - SUM(cost) - SUM(shipping)) AS gross_profit,
    YEAR(NOW()) AS year,
    MONTH(NOW()) AS month
FROM usatocn2013.orders
WHERE client <> '张三'
AND YEAR(created_time) = YEAR(NOW())
AND MONTH(created_time) = MONTH(NOW())
GROUP BY MONTH(created_time);
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
AND MONTH(created_time) = MONTH(NOW())
AND YEAR(created_time) = YEAR(NOW())
GROUP BY DATE(created_time)
ORDER BY DATE(created_time);
"""
