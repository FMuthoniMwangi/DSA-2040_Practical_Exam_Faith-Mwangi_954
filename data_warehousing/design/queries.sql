/*
    queries.sql contains example SQL queries to test and demonstrate the star schema functionality.
    These queries help validate relationships, check data integrity, and showcase reporting capabilities.
*/


SELECT * 
FROM Sales_Fact;


---------------------------------------------------
-- 2. Join Fact table with all Dimension tables
---------------------------------------------------
SELECT 
    sf.SalesID,
    dp.ProductName,
    dc.FirstName + ' ' + dc.LastName AS CustomerName,
    ds.StoreName,
    dd.DateValue,
    sf.QuantitySold,
    sf.TotalSales
FROM Sales_Fact sf
JOIN Dim_Product dp ON sf.ProductKey = dp.ProductKey
JOIN Dim_Customer dc ON sf.CustomerKey = dc.CustomerKey
JOIN Dim_Store ds ON sf.StoreKey = ds.StoreKey
JOIN Dim_Date dd ON sf.DateKey = dd.DateKey;


---------------------------------------------------
-- 3. Total Sales by Product
---------------------------------------------------
SELECT 
    dp.ProductName,
    SUM(sf.TotalSales) AS TotalSalesAmount
FROM Sales_Fact sf
JOIN Dim_Product dp ON sf.ProductKey = dp.ProductKey
GROUP BY dp.ProductName
ORDER BY TotalSalesAmount DESC;


---------------------------------------------------
-- 4. Monthly Sales Trend
---------------------------------------------------
SELECT 
    dd.Year,
    dd.Month,
    SUM(sf.TotalSales) AS MonthlySales
FROM Sales_Fact sf
JOIN Dim_Date dd ON sf.DateKey = dd.DateKey
GROUP BY dd.Year, dd.Month
ORDER BY dd.Year, dd.Month;


---------------------------------------------------
-- 5. Top Customers by Sales
---------------------------------------------------
SELECT 
    dc.FirstName + ' ' + dc.LastName AS CustomerName,
    SUM(sf.TotalSales) AS TotalSpent
FROM Sales_Fact sf
JOIN Dim_Customer dc ON sf.CustomerKey = dc.CustomerKey
GROUP BY dc.FirstName, dc.LastName
ORDER BY TotalSpent DESC;
