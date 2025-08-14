import dash
from dash import dcc, html, dash_table
import pandas as pd
import sqlite3
import plotly.express as px

DB_FILE_PATH = "data_warehousing/etl/retail_dw.db"

# Connect to DB and load aggregated data
conn = sqlite3.connect(DB_FILE_PATH)
df = pd.read_sql("""
SELECT c.Country, f.Category, SUM(f.TotalSales) AS TotalSales
FROM SalesFact f
JOIN CustomerDim c ON f.CustomerKey = c.CustomerKey
GROUP BY c.Country, f.Category
HAVING TotalSales > 0
""", conn)
conn.close()

# Get only countries with data
countries = sorted(df["Country"].unique())
categories = sorted(df["Category"].unique())

app = dash.Dash(__name__)
app.title = "OLAP Dashboard"

app.layout = html.Div([
    html.H1(
        "💹 OLAP Sales Dashboard",
        style={"textAlign": "center", "color": "#2E86C1", "marginBottom": "20px"}
    ),

    html.Div([
        html.Div([
            html.Label("Select Country", style={"fontWeight": "bold", "color": "#34495E"}),
            dcc.Dropdown(
                id="country-filter",
                options=[{"label": c, "value": c} for c in countries],
                value=countries[0],
                clearable=False
            )
        ], style={"width": "48%", "display": "inline-block"}),

        html.Div([
            html.Label("Select Category", style={"fontWeight": "bold", "color": "#34495E"}),
            dcc.Dropdown(
                id="category-filter",
                options=[{"label": c, "value": c} for c in categories],
                value=categories[0],
                clearable=False
            )
        ], style={"width": "48%", "display": "inline-block", "float": "right"})
    ], style={"marginBottom": "20px"}),

    html.Div([
        dcc.Graph(id="sales-chart", style={"border": "1px solid #ddd", "borderRadius": "10px"})
    ], style={"marginBottom": "30px"}),

    dash_table.DataTable(
        id="sales-table",
        columns=[{"name": i, "id": i} for i in df.columns],
        style_table={"overflowX": "auto", "border": "1px solid #ddd"},
        style_header={"backgroundColor": "#2E86C1", "fontWeight": "bold", "color": "white"},
        style_cell={"textAlign": "left", "padding": "8px"}
    )
], style={"margin": "20px", "fontFamily": "Arial"})

@app.callback(
    [dash.Output("sales-chart", "figure"),
     dash.Output("sales-table", "data")],
    [dash.Input("country-filter", "value"),
     dash.Input("category-filter", "value")]
)
def update_dashboard(selected_country, selected_category):
    filtered_df = df.copy()

    if selected_country:
        filtered_df = filtered_df[filtered_df["Country"] == selected_country]
    if selected_category:
        filtered_df = filtered_df[filtered_df["Category"] == selected_category]

    fig = px.bar(
        filtered_df,
        x="Category",
        y="TotalSales",
        color="Country",
        title=f"Total Sales in {selected_country} - {selected_category}",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")

    return fig, filtered_df.to_dict("records")

if __name__ == "__main__":
    app.run_server(debug=True)
