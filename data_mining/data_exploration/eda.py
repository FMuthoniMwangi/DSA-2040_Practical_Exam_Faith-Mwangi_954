# data_mining/eda.py
import os
import logging
import seaborn as sns
import matplotlib.pyplot as plt

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Output path
OUTPUT_DIR = os.path.join("data_exploration", "task1_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run(df_raw, df_scaled):
    """Generate EDA plots on raw and scaled DataFrames."""
    logging.info("Starting EDA and generating visualizations...")

    # Missing values heatmap
    plt.figure(figsize=(6,4))
    sns.heatmap(df_raw.isnull(), cbar=False, cmap="viridis")
    missing_path = os.path.join(OUTPUT_DIR, "iris_missing_values.png")
    plt.title("Missing Values Heatmap")
    plt.savefig(missing_path)
    plt.close()
    logging.info(f"Saved missing values heatmap to {missing_path}")

    # Pairplots
    pairplot_raw_path = os.path.join(OUTPUT_DIR, "iris_pairplot_raw.png")
    sns.pairplot(df_raw, hue="species", diag_kind="hist")
    plt.suptitle("Raw Data Pairplot", y=1.02)
    plt.savefig(pairplot_raw_path)
    plt.close()
    logging.info(f"Saved raw pairplot to {pairplot_raw_path}")

    pairplot_scaled_path = os.path.join(OUTPUT_DIR, "iris_pairplot_scaled.png")
    sns.pairplot(df_scaled, hue="species", diag_kind="hist")
    plt.suptitle("Scaled Data Pairplot", y=1.02)
    plt.savefig(pairplot_scaled_path)
    plt.close()
    logging.info(f"Saved scaled pairplot to {pairplot_scaled_path}")

    # Correlation heatmap
    plt.figure(figsize=(8,6))
    sns.heatmap(df_scaled.drop(columns="species").corr(), annot=True, cmap="coolwarm")
    heatmap_path = os.path.join(OUTPUT_DIR, "iris_correlation_heatmap.png")
    plt.title("Correlation Heatmap")
    plt.savefig(heatmap_path)
    plt.close()
    logging.info(f"Saved correlation heatmap to {heatmap_path}")

    logging.info("EDA complete.")
