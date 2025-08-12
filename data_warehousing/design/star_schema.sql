CREATE TABLE Dim_Product (
    ProductKey     INT PRIMARY KEY IDENTITY(1,1),
    ProductName    VARCHAR(100) NOT NULL,
    Category       VARCHAR(50),
    SubCategory    VARCHAR(50)
);

CREATE TABLE Dim_Customer (
    CustomerKey    INT PRIMARY KEY IDENTITY(1,1),
    FirstName      VARCHAR(50) NOT NULL,
    LastName       VARCHAR(50) NOT NULL,
    Gender         VARCHAR(10),
    Age            INT,
    Country        VARCHAR(50)
);

CREATE TABLE Dim_Date (
    DateKey        INT PRIMARY KEY,
    DateValue      DATE NOT NULL,
    Day            INT NOT NULL,
    Month          INT NOT NULL,
    Quarter        INT NOT NULL,
    Year           INT NOT NULL
);

CREATE TABLE Dim_Store (
    StoreKey       INT PRIMARY KEY IDENTITY(1,1),
    StoreName      VARCHAR(100) NOT NULL,
    City           VARCHAR(50),
    Country        VARCHAR(50)
);

CREATE TABLE Sales_Fact (
    SalesID        INT PRIMARY KEY IDENTITY(1,1),
    DateKey        INT NOT NULL,
    ProductKey     INT NOT NULL,
    CustomerKey    INT NOT NULL,
    StoreKey       INT NOT NULL,
    QuantitySold   INT NOT NULL,
    TotalSales     DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (DateKey) REFERENCES Dim_Date(DateKey),
    FOREIGN KEY (ProductKey) REFERENCES Dim_Product(ProductKey),
    FOREIGN KEY (CustomerKey) REFERENCES Dim_Customer(CustomerKey),
    FOREIGN KEY (StoreKey) REFERENCES Dim_Store(StoreKey)
);
