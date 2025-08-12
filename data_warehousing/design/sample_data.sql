/*
    The purpose of the sample_data.sql is to populate the dimension and fact tables with test data
    for validating the star schema structure and relationships.
*/


INSERT INTO Dim_Product (ProductName, Category, SubCategory)
VALUES ('Laptop', 'Electronics', 'Computers');

INSERT INTO Dim_Customer (FirstName, LastName, Gender, Age, Country)
VALUES ('Faith', 'Mwangi', 'Female', 18, 'KE');

INSERT INTO Dim_Date (DateKey, DateValue, Day, Month, Quarter, Year)
VALUES (20240801, '2024-08-01', 1, 8, 3, 2024);

INSERT INTO Dim_Store (StoreName, City, Country)
VALUES ('Kilimani', 'Nairobi', 'KE');

INSERT INTO Sales_Fact (DateKey, ProductKey, CustomerKey, StoreKey, QuantitySold, TotalSales)
VALUES (20240801, 1, 1, 1, 2, 2000.00);
