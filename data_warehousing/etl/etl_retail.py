"""
ETL (Extract, Transform, Load) for the Online Retail dataset.
Generates cleaned CSV, HTML profile, and loads SQLite DB.
"""

import pandas as pd
import sqlite3
import logging
import os
from ydata_profiling import ProfileReport

# ------------------ CONFIG ------------------
RAW_FILE_PATH = "data_warehousing/data/raw/OnlineRetail.xlsx"
DB_FILE_PATH = "data_warehousing/etl/retail_dw.db"
LOG_FILE = "data_warehousing/etl/etl_log.txt"
PROCESSED_DIR = "data_warehousing/data/processed"
CLEANED_CSV = "OnlineRetail_cleaned.csv"
PROFILE_PATH = "data_warehousing/etl/OnlineRetail_cleaned_summary.html"

os.makedirs("data_warehousing/etl", exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ------------------ ETL FUNCTIONS ------------------

def extract_data():
    """Extract step: read Excel and clean missing critical values"""
    try:
        df = pd.read_excel(RAW_FILE_PATH)
        logging.info(f"Data extracted: {df.shape[0]} rows, {df.shape[1]} columns.")
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
        df.dropna(subset=['InvoiceNo', 'StockCode', 'InvoiceDate', 'UnitPrice', 'Quantity', 'CustomerID'], inplace=True)
        logging.info(f"After dropping missing critical values: {df.shape[0]} rows.")
        return df
    except Exception as e:
        logging.error(f"Error during extraction: {e}")
        raise

# Assign product categories (for OLAP slice)
def assign_category(description):
    description = str(description).lower()
    if any(word in description for word in ['laptop', 'mouse', 'keyboard']):
        return 'Electronics'
    elif any(word in description for word in ['t-shirt', 'dress', 'shirt']):
        return 'Apparel'
    elif any(word in description for word in ['book']):
        return 'Books'
    else:
        return 'Other'


def transform_data(df):
    """Transform step: remove invalid rows, calculate TotalSales, prepare dimensions"""
    try:
        # Remove negative or zero values
        df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)].copy()
        logging.info(f"After removing invalid rows: {df.shape[0]} rows.")

        if df.empty:
            logging.warning("DataFrame is empty after removing invalid rows. Skipping further transformations.")
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

        df['TotalSales'] = df['Quantity'] * df['UnitPrice']

        # Add category column
        df['Category'] = df['Description'].apply(assign_category)


        # Prepare Customer Dimension
        customer_dim = (
            df.groupby(['CustomerID', 'Country'])
            .agg(
                TotalPurchases=('TotalSales', 'sum'),
                Transactions=('InvoiceNo', 'nunique')
            )
            .reset_index()
        )
        customer_dim['CustomerKey'] = customer_dim.index + 1  # surrogate key

        # Prepare Time Dimension
        time_dim = df[['InvoiceDate']].drop_duplicates().copy()
        time_dim['DateKey'] = time_dim['InvoiceDate'].dt.strftime('%Y%m%d').astype(int)
        time_dim['Day'] = time_dim['InvoiceDate'].dt.day
        time_dim['Month'] = time_dim['InvoiceDate'].dt.month
        time_dim['Quarter'] = time_dim['InvoiceDate'].dt.quarter
        time_dim['Year'] = time_dim['InvoiceDate'].dt.year

        # Prepare Fact Table
        fact_df = df.merge(customer_dim[['CustomerID', 'CustomerKey']], on='CustomerID', how='left')
        fact_df = fact_df.merge(time_dim[['InvoiceDate', 'DateKey']], on='InvoiceDate', how='left')
        fact_df = fact_df[[
            'InvoiceNo', 'StockCode', 'Description', 'Quantity',
            'UnitPrice', 'TotalSales', 'CustomerKey', 'DateKey',
            'CustomerID', 'Country', 'InvoiceDate'
        ]]

        # Save cleaned CSV
        cleaned_path = os.path.join(PROCESSED_DIR, CLEANED_CSV)
        fact_df.to_csv(cleaned_path, index=False)
        logging.info(f"Cleaned CSV saved to {cleaned_path}")

        # Generate HTML profile
        profile = ProfileReport(df, title="Online Retail Data Profile", explorative=True)
        profile.to_file(PROFILE_PATH)
        logging.info(f"Profile report saved to {PROFILE_PATH}")

        return fact_df, customer_dim, time_dim

    except Exception as e:
        logging.error(f"Error during transformation: {e}")
        raise

def load_data(fact_df, customer_dim, time_dim):
    """Load step: save fact and dimension tables into SQLite"""
    try:
        if fact_df.empty or customer_dim.empty or time_dim.empty:
            logging.warning("One or more DataFrames are empty. Skipping DB load.")
            return

        conn = sqlite3.connect(DB_FILE_PATH)
        fact_df.to_sql('SalesFact', conn, if_exists='replace', index=False)
        customer_dim.to_sql('CustomerDim', conn, if_exists='replace', index=False)
        time_dim.to_sql('TimeDim', conn, if_exists='replace', index=False)
        conn.close()
        logging.info(f"Data loaded into DB: Fact {fact_df.shape[0]}, CustomerDim {customer_dim.shape[0]}, TimeDim {time_dim.shape[0]}")
    except Exception as e:
        logging.error(f"Error during load: {e}")
        raise

def run_etl():
    logging.info("ETL process started.")
    try:
        raw_df = extract_data()
        fact_df, customer_dim, time_dim = transform_data(raw_df)
        load_data(fact_df, customer_dim, time_dim)
        logging.info("ETL process completed successfully.")
    except Exception as e:
        logging.error(f"ETL process failed: {e}")
        raise

if __name__ == "__main__":
    run_etl()
