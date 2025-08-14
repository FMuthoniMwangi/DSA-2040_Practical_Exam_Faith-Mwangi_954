"""
Create HTML + PNG + PDF dashboard for top-10 countries (by total sales).
Outputs:
 - task3_olap/dashboard.html
 - task3_olap/chart_1_top10_countries.png
 - task3_olap/chart_2_stacked_by_category.png
 - task3_olap/chart_3_monthly_trend.png
 - task3_olap/olap_dashboard.pdf
"""

import os
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from PIL import Image

# ---------- CONFIG ----------
DB_FILE_PATH = "data_warehousing/etl/retail_dw.db"   # adjust if needed
OUT_DIR = "data_warehousing/olap"
HTML_PATH = os.path.join(OUT_DIR, "dashboard.html")
PDF_PATH = os.path.join(OUT_DIR, "olap_dashboard.pdf")
PNG1 = os.path.join(OUT_DIR, "chart_1_top10_countries.png")
PNG2 = os.path.join(OUT_DIR, "chart_2_stacked_by_category.png")
PNG3 = os.path.join(OUT_DIR, "chart_3_monthly_trend.png")

os.makedirs(OUT_DIR, exist_ok=True)

# ---------- LOAD DATA ----------
if not os.path.exists(DB_FILE_PATH):
    raise SystemExit(f"Database not found at {DB_FILE_PATH}. Run ETL to create it first.")

conn = sqlite3.connect(DB_FILE_PATH)

# Aggregate total sales by country
tot_by_country = pd.read_sql_query("""
SELECT c.Country, SUM(f.TotalSales) AS TotalSales
FROM SalesFact f
JOIN CustomerDim c ON f.CustomerKey = c.CustomerKey
GROUP BY c.Country
HAVING TotalSales > 0
ORDER BY TotalSales DESC;
""", conn)

if tot_by_country.empty:
    raise SystemExit("No sales data found in DB.")

# Top 10 countries
top10 = tot_by_country.head(10).copy()
top_countries = top10['Country'].tolist()

# Data for stacked category-by-country (only top 10)
stacked_q = f"""
SELECT c.Country, f.Category, SUM(f.TotalSales) AS TotalSales
FROM SalesFact f
JOIN CustomerDim c ON f.CustomerKey = c.CustomerKey
WHERE c.Country IN ({','.join(['?']*len(top_countries))})
GROUP BY c.Country, f.Category;
"""
stacked_df = pd.read_sql_query(stacked_q, conn, params=top_countries)

# Monthly trend for top10 countries (time series)
trend_q = f"""
SELECT t.Year, t.Month, c.Country, SUM(f.TotalSales) AS TotalSales
FROM SalesFact f
JOIN TimeDim t ON f.DateKey = t.DateKey
JOIN CustomerDim c ON f.CustomerKey = c.CustomerKey
WHERE c.Country IN ({','.join(['?']*len(top_countries))})
GROUP BY t.Year, t.Month, c.Country
ORDER BY t.Year, t.Month;
"""
trend_df = pd.read_sql_query(trend_q, conn, params=top_countries)

conn.close()

# ---------- CHART 1: Bar - Top 10 Countries ----------
# Color palette like Power BI qualitative
colors = px.colors.qualitative.Bold

fig1 = px.bar(
    top10,
    x='Country',
    y='TotalSales',
    title='Top 10 Countries by Total Sales',
    labels={'TotalSales':'Total Sales', 'Country':'Country'},
)
fig1.update_traces(marker_color=colors * (len(top10)//len(colors) + 1))
fig1.update_layout(plot_bgcolor='white', paper_bgcolor='white', title_x=0.5)
fig1.update_xaxes(tickangle= -45)

# Save PNG
fig1.write_image(PNG1, width=1200, height=600, scale=2)

# ---------- CHART 2: Stacked Bar - Category contributions (Top 10) ----------
# Pivot to wide for stacked bars
stacked_pivot = stacked_df.pivot_table(index='Country', columns='Category', values='TotalSales', aggfunc='sum').fillna(0)
# Keep top countries order
stacked_pivot = stacked_pivot.reindex(top_countries)

fig2 = go.Figure()
cat_list = stacked_pivot.columns.tolist()
color_cycle = px.colors.qualitative.Safe
for i, cat in enumerate(cat_list):
    fig2.add_trace(go.Bar(
        name=cat,
        x=stacked_pivot.index,
        y=stacked_pivot[cat],
        marker_color=color_cycle[i % len(color_cycle)]
    ))
fig2.update_layout(barmode='stack', title='Category Sales Breakdown (Top 10 Countries)', title_x=0.5)
fig2.update_layout(xaxis_tickangle=-45, plot_bgcolor='white', paper_bgcolor='white')
fig2.update_yaxes(title_text="Total Sales")

fig2.write_image(PNG2, width=1200, height=700, scale=2)

# ---------- CHART 3: Line Chart - Monthly trend (Top 10 combined) ----------
# Create a monthly date for plotting: use Year-Month first day
trend_df['MonthStart'] = pd.to_datetime(trend_df['Year'].astype(int).astype(str) + '-' + trend_df['Month'].astype(int).astype(str) + '-01')
# Aggregate across countries or plot multiple lines (we'll plot one line per country)
fig3 = px.line(
    trend_df,
    x='MonthStart',
    y='TotalSales',
    color='Country',
    title='Monthly Sales Trend (Top 10 Countries)',
    labels={'MonthStart':'Month','TotalSales':'Total Sales'}
)
fig3.update_layout(plot_bgcolor='white', paper_bgcolor='white', title_x=0.5)
fig3.update_xaxes(rangeslider_visible=True)

fig3.write_image(PNG3, width=1400, height=700, scale=2)

# ---------- COMBINE INTO HTML ----------
# Create HTML snippets for each figure (embed plotly CDN)
html_parts = []
for fig, caption in [(fig1, "Top 10 Countries by Sales"), (fig2, "Category Breakdown by Country"), (fig3, "Monthly Sales Trend (Top 10)")]:
    html_parts.append(f"<h2 style='font-family:Arial; color:#2E86C1; text-align:center'>{caption}</h2>")
    html_parts.append(fig.to_html(full_html=False, include_plotlyjs='cdn'))

# Add a header and timestamp
header = f"""
<html>
<head>
  <meta charset="utf-8" />
  <title>OLAP Dashboard - Top 10 Countries</title>
</head>
<body style="font-family: Arial; margin: 20px; background-color:#F7F9FB">
  <div style="text-align:center;">
    <h1 style="color:#0B5345">OLAP Dashboard — Top 10 Countries</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
  </div>
  <div style="max-width:1200px; margin: 0 auto;">
"""

footer = """
  </div>
  <div style="text-align:center; color: #666; margin-top:40px;">
    <small>Data source: retail_dw.db — processed with ETL pipeline</small>
  </div>
</body>
</html>
"""

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(header + "\n".join(html_parts) + footer)

print("HTML dashboard written to:", HTML_PATH)
print("PNGs:", PNG1, PNG2, PNG3)

# ---------- COMBINE PNGS INTO PDF ----------
pngs = [PNG1, PNG2, PNG3]
images = []
for p in pngs:
    img = Image.open(p).convert('RGB')
    images.append(img)

if images:
    images[0].save(PDF_PATH, save_all=True, append_images=images[1:], quality=95)
    print("PDF exported to:", PDF_PATH)
else:
    print("No PNGs found to combine into PDF.")
