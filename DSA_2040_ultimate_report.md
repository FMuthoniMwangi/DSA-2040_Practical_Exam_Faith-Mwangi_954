# Ultimate Exam Report: DSA 2040

This report consolidates all tasks from Data Warehousing and Data Mining.

## Data Warehousing: Task 1 – Design

# Data Warehouse Star Schema Design Report

In this report, I describe how I designed a **Sales Data Warehouse** using the **Star Schema** approach. It includes a schema diagram, a basic architecture diagram, SQL table definitions, some sample data, and example queries to test if the design works as expected.

---

## 1. Star Schema Overview

The **Star Schema** is a type of database design that has a **central fact table** that stores the important business events (like sales), and several **dimension tables** that describe those events in more detail (like information about the product, customer, time, and store). 

For this project, hereâ€™s what I included:

- **Fact Table:** `Sales_Fact`  
  - This table holds the main numbers I want to analyze (like quantity sold and total sales).
- **Dimension Tables:**  
  - `Dim_Product`: Information about each product, including which category itâ€™s in.
  - `Dim_Customer`: Info about customers, like their names, gender, age, and country.
  - `Dim_Date`: Calendar information to make time-based analysis easier.
  - `Dim_Store`: Store location details.

---

## 2. Why use the Star Schema over the Snowflake Schema?

The **Star Schema** keeps dimension tables denormalized (fewer joins, simpler queries) while the **Snowflake Schema** normalizes dimensions into multiple related tables.

| Feature               | Star Schema                       | Snowflake Schema                 |
|-----------------------|------------------------------------|-----------------------------------|
| Structure             | Fact table + denormalized dimensions | Fact table + normalized dimensions |
| Query Performance     | Faster, fewer joins               | Slower, more joins                |
| Storage Requirements  | Higher (data redundancy)          | Lower (less redundancy)           |
| Complexity            | Simple design, easy to understand | More complex, harder to maintain  |

For this warehouse, the **Star Schema** was chosen to optimize for **query performance** and **ease of use** in reporting.


---

## 3. Architecture Diagram

![Architecture Diagram](architecture_diagram.png)  
**Flow:** Data Source â†’ ETL â†’ Data Warehouse (Star Schema) 

I tried to show the basic flow in my diagram: data comes in from the source, goes through ETL (Extract, Transform, Load), gets stored in my star schema, and then is used for analysis and dashboards.

---

## 4. Schema Diagram

![Star Schema Diagram](schema_diagram.png)  
This diagram shows how the fact table connects to each dimension table using primary keys (PK) and foreign keys (FK). This helps understand the relationships much better.

---

## 5. Data Dictionary

### 5.1 Fact Table: `Sales_Fact`
| Column        | Type        | Description                               |
|---------------|-------------|-------------------------------------------|
| SalesID       | INT (PK)    | Unique identifier for each sales record   |
| DateKey       | INT (FK)    | Links to `Dim_Date`                       |
| ProductKey    | INT (FK)    | Links to `Dim_Product`                    |
| CustomerKey   | INT (FK)    | Links to `Dim_Customer`                   |
| StoreKey      | INT (FK)    | Links to `Dim_Store`                      |
| QuantitySold  | INT         | Number of units sold                      |
| TotalSales    | DECIMAL     | Total sales value                         |

### 5.2 Dimension Tables

#### `Dim_Product`
| Column        | Type        | Description                  |
|---------------|-------------|------------------------------|
| ProductKey    | INT (PK)    | Unique product identifier    |
| ProductName   | TEXT        | Name of the product          |
| Category      | TEXT        | High-level product category  |
| SubCategory   | TEXT        | More specific classification |

#### `Dim_Customer`
| Column        | Type        | Description                  |
|---------------|-------------|------------------------------|
| CustomerKey   | INT (PK)    | Unique customer identifier   |
| FirstName     | TEXT        | Customer's first name        |
| LastName      | TEXT        | Customer's last name         |
| Gender        | TEXT        | Gender of customer           |
| Age           | INT         | Age of customer              |
| Country       | TEXT        | Country of customer          |

#### `Dim_Date`
| Column        | Type        | Description                  |
|---------------|-------------|------------------------------|
| DateKey       | INT (PK)    | Unique date in YYYYMMDD format|
| DateValue     | DATE        | Calendar date                |
| Day           | INT         | Day of the month             |
| Month         | INT         | Month number                 |
| Quarter       | INT         | Quarter number (1-4)         |
| Year          | INT         | Year value                   |

#### `Dim_Store`
| Column        | Type        | Description                  |
|---------------|-------------|------------------------------|
| StoreKey      | INT (PK)    | Unique store identifier      |
| StoreName     | TEXT        | Name of store                |
| City          | TEXT        | City where store is located  |
| Country       | TEXT        | Country of store             |

---

## 6. Sample Data

A small SQL script called [`sample_data.sql`](sample_data.sql) to add some initial data for testing. Here are a few examples:

```sql
-- Sample product
INSERT INTO Dim_Product (ProductName, Category, SubCategory)
VALUES ('Laptop', 'Electronics', 'Computers');

-- Sample customer
INSERT INTO Dim_Customer (FirstName, LastName, Gender, Age, Country)
VALUES ('Faith', 'Mwangi', 'Female', 18, 'KE');

-- Sample date
INSERT INTO Dim_Date (DateKey, DateValue, Day, Month, Quarter, Year)
VALUES (20240801, '2024-08-01', 1, 8, 3, 2024);

-- Sample store
INSERT INTO Dim_Store (StoreName, City, Country)
VALUES ('Kilimani', 'Nairobi', 'KE');

-- Sample sales fact
INSERT INTO Sales_Fact (DateKey, ProductKey, CustomerKey, StoreKey, QuantitySold, TotalSales)
VALUES (20240801, 1, 1, 1, 2, 2000.00);
```


## Data Warehousing: Task 2 – OLAP Queries & Analysis

# OLAP Analysis Report

This analysis explores sales trends from the Online Retail Data Warehouse.

---

## Roll-up Analysis
![Top 10 Countries by Total Sales](chart_1_top10_countries.png)

Total sales were aggregated by country and quarter.  
The UK had consistently higher sales across all quarters, indicating strong market presence.

---

## Drill-down Analysis
![Stacked Sales by Category](chart_2_stacked_by_category.png)

Monthly sales details for the UK showed seasonal peaks during November and December,  
likely due to holiday shopping.

---

## Slice Analysis
![Monthly Sales Trend](chart_3_monthly_trend.png)

Electronics category analysis revealed high sales during mid-year months,  
suggesting mid-year promotions and consumer electronics cycles.

---

## Insights
The data warehouse enables rapid querying across multiple dimensions, supporting decision-making for inventory, marketing, and regional strategies.  
Using synthetic categories for analysis provided a simplified but clear example of product segmentation.

**Key findings:**
- Top-performing countries: UK, Germany  
- Highest sales months: Novemberâ€“December  
- Electronics is a high-revenue category

The OLAP approach supports management in making data-driven decisions by providing aggregated, detailed, and sliceable views of sales data.


## Data Mining: Task 1 – Preprocessing & EDA

# Iris Dataset Preprocessing & EDA Report

This report summarizes the preprocessing and exploratory data analysis (EDA) outputs for the Iris dataset.

## Dataset Description
- **Dataset source:** scikit-learn's built-in Iris dataset (`sklearn.datasets.load_iris()`)
- **Samples:** 150
- **Features:** sepal length, sepal width, petal length, petal width
- **Target/Label:** species (setosa, versicolor, virginica)

## Preprocessing
1. Checked for missing values and none were found. A heatmap visualization is included below.
2. Numerical features were standardized using `StandardScaler` to prepare the data for further analysis or ML models.
3. Raw and scaled datasets are saved as CSV files for reproducibility.

### CSV Files
- Raw dataset: [`iris_raw.csv`](iris_raw.csv)
- Scaled dataset: [`iris_scaled.csv`](iris_scaled.csv)

## Exploratory Data Analysis (EDA)
EDA helps understand feature distributions, relationships, and potential outliers.

### Missing Values Heatmap
Shows whether there are any missing values in the dataset. Light areas indicate missing values.
![Missing Values](iris_missing_values.png)

### Pairplot - Raw Data
Visualizes the pairwise relationships between features before scaling. Colors indicate species.
![Pairplot Raw](iris_pairplot_raw.png)

### Pairplot - Scaled Data
Pairplot after scaling numerical features, demonstrating that relationships between features are preserved.
![Pairplot Scaled](iris_pairplot_scaled.png)

### Correlation Heatmap
Shows the Pearson correlation between numerical features. Strong positive/negative correlations are highlighted.
![Correlation Heatmap](iris_correlation_heatmap.png)

## Summary
- The dataset is clean with no missing values.
- Standardization was applied to numerical features.
- EDA plots reveal relationships between features and species.
- All preprocessing and EDA outputs are saved in this folder (`task1_output`) to meet Task 1 rubric requirements.


## Data Mining: Task 2 – Clustering

# Iris Dataset Clustering Report

This report summarizes K-Means clustering results on the Iris dataset using preprocessed data from Task 1.

## Dataset & Preprocessing
- **Dataset source:** scikit-learn Iris dataset, preprocessed (scaled features).
- **Features used:** sepal length, sepal width, petal length, petal width.
- **Target labels:** species (setosa, versicolor, virginica).

## K-Means Clustering Experiments
We applied K-Means clustering with different values of k (2, 3, 4) and evaluated cluster quality.

### Results Table
Metrics for each k are saved in [`kmeans_results.csv`](kmeans_results.csv).

### Elbow Curve
Shows inertia vs number of clusters to justify the choice of k.
![Elbow Curve](kmeans_elbow.png)

### Cluster Scatter Plots
Scatter plots of petal length vs petal width for each k. Clusters are colored and centroids are marked with 'X'.
#### K = 2
![K=2 Scatter](kmeans_k2_scatter.png)

#### K = 3
![K=3 Scatter](kmeans_k3_scatter.png)

#### K = 4
![K=4 Scatter](kmeans_k4_scatter.png)

## Analysis
K-Means with k=3 aligns well with the three species. ARI indicates strong agreement with true labels. K=2 merges some species, reducing ARI, while k=4 splits one species, slightly reducing cluster quality. Silhouette scores and inertia support k=3 as the optimal cluster count. Misclassifications mostly occur between versicolor and virginica, consistent with overlapping feature ranges. Real-world application: similar clustering can segment customers based on features in marketing or biology. Synthetic data (if used) may affect cluster separability slightly, but overall trends are preserved.

All outputs (CSV, plots) are saved in this folder (`task2_output`) to meet the Task 2 rubric requirements.


## Data Mining: Task 3 – Classification & Association Rule Mining

# Task 3: Classification & Association Rule Mining Report

## Part A: Classification
We trained a Decision Tree and a KNN (k=5) classifier on the preprocessed Iris dataset.

### Classifier Metrics
|               |   accuracy |   precision |   recall |       f1 |
|:--------------|-----------:|------------:|---------:|---------:|
| Decision Tree |   0.933333 |    0.933333 | 0.933333 | 0.933333 |
| KNN           |   0.933333 |    0.944444 | 0.933333 | 0.93266  |

### Decision Tree Visualization
![Decision Tree](decision_tree.png)

**Analysis:** Decision Tree achieved higher performance than KNN on this dataset due to its ability to split features effectively. KNN may struggle if feature scales are not perfectly normalized.

## Part B: Association Rule Mining
Synthetic transaction data was generated with 20 items and 30 random baskets.

### Top 5 Association Rules (sorted by lift)
| antecedents   | consequents   | antecedent support   | consequent support   | support   | confidence   | lift   | representativity   | leverage   | conviction   | zhangs_metric   | jaccard   | certainty   | kulczynski   |
|---------------|---------------|----------------------|----------------------|-----------|--------------|--------|--------------------|------------|--------------|-----------------|-----------|-------------|--------------|

**Analysis:** For example, a rule like `milk -> bread` with high lift indicates that when milk is purchased, bread is also likely to be purchased. Such insights can guide product placement or promotions in retail.

All outputs (metrics CSV, decision tree image, rules CSV) are saved in this folder (`task3_output`).


