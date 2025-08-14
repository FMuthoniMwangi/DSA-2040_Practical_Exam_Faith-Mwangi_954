-- Roll-up: Total sales by Country and Quarter
SELECT c.Country, t.Quarter, SUM(f.TotalSales) AS TotalSales
FROM SalesFact f
JOIN CustomerDim c ON f.CustomerKey = c.CustomerKey
JOIN TimeDim t ON f.DateKey = t.DateKey
GROUP BY c.Country, t.Quarter
ORDER BY c.Country, t.Quarter;

-- Drill-down: Sales details for a specific country (e.g., UK) by Month
SELECT t.Year, t.Month, SUM(f.TotalSales) AS TotalSales
FROM SalesFact f
JOIN CustomerDim c ON f.CustomerKey = c.CustomerKey
JOIN TimeDim t ON f.DateKey = t.DateKey
WHERE c.Country = 'United Kingdom'
GROUP BY t.Year, t.Month
ORDER BY t.Year, t.Month;

-- Slice: Total sales for Electronics category
SELECT t.Year, t.Month, SUM(f.TotalSales) AS TotalSales
FROM SalesFact f
JOIN TimeDim t ON f.DateKey = t.DateKey
WHERE f.Category = 'Electronics'
GROUP BY t.Year, t.Month
ORDER BY t.Year, t.Month;
