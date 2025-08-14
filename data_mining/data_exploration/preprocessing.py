# data_mining/preprocessing.py
import os
import logging
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Output path
OUTPUT_DIR = os.path.join("data_exploration", "task1_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run(csv_path=None):
    """Load, preprocess Iris dataset, save CSVs, and return DataFrames."""
    logging.info("Loading Iris dataset...")

    if csv_path and os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        logging.info(f"Loaded CSV from {csv_path}")
    else:
        iris = load_iris()
        df = pd.DataFrame(iris.data, columns=iris.feature_names)
        df["species"] = pd.Categorical.from_codes(iris.target, iris.target_names)
        logging.info("Loaded sklearn Iris dataset")

    # Scale numerical features
    features = df.columns[:-1]  # exclude species
    scaler = StandardScaler()
    df_scaled = df.copy()
    df_scaled[features] = scaler.fit_transform(df[features])
    logging.info("Scaled numerical features using StandardScaler")

    # Save CSVs
    raw_path = os.path.join(OUTPUT_DIR, "iris_raw.csv")
    scaled_path = os.path.join(OUTPUT_DIR, "iris_scaled.csv")
    df.to_csv(raw_path, index=False)
    df_scaled.to_csv(scaled_path, index=False)
    logging.info(f"Saved raw CSV to {raw_path}")
    logging.info(f"Saved scaled CSV to {scaled_path}")

    return df, df_scaled
