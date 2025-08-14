import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_FILE_PATH = "data_warehousing/etl/retail_dw.db"

# Connect to database
conn = sqlite3.connect(DB_FILE_PATH)

# Roll-up: Total sales by Country and Quarter
rollup_query = """
SELECT c.Country, t.Quarter, SUM(f.TotalSales) AS TotalSales
FROM SalesFact f
JOIN CustomerDim c ON f.CustomerKey = c.CustomerKey
JOIN TimeDim t ON f.DateKey = t.DateKey
GROUP BY c.Country, t.Quarter
ORDER BY c.Country, t.Quarter;
"""
rollup_df = pd.read_sql_query(rollup_query, conn)

# Bar chart of sales by Country
summary_df = rollup_df.groupby('Country')['TotalSales'].sum().sort_values(ascending=False)
plt.figure(figsize=(10,6))
summary_df.plot(kind='bar', color='skyblue')
plt.title("Total Sales by Country")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig("data_warehousing/OLAP/olap_visuals.png")
plt.show()

conn.close()
