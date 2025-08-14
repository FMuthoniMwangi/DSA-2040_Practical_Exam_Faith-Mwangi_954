# data_mining/report.py
import os

# Output path
OUTPUT_DIR = os.path.join("data_mining", "task1_output")

def generate_md_report():
    """Generate a Markdown report of preprocessing & EDA outputs with explanations."""
    report_path = os.path.join(OUTPUT_DIR, "iris_report.md")

    with open(report_path, "w") as f:
        f.write("# Iris Dataset Preprocessing & EDA Report\n\n")
        f.write("This report summarizes the preprocessing and exploratory data analysis (EDA) outputs for the Iris dataset.\n\n")

        f.write("## Dataset Description\n")
        f.write("- **Dataset source:** scikit-learn's built-in Iris dataset (`sklearn.datasets.load_iris()`)\n")
        f.write("- **Samples:** 150\n")
        f.write("- **Features:** sepal length, sepal width, petal length, petal width\n")
        f.write("- **Target/Label:** species (setosa, versicolor, virginica)\n\n")

        f.write("## Preprocessing\n")
        f.write("1. Checked for missing values and none were found. A heatmap visualization is included below.\n")
        f.write("2. Numerical features were standardized using `StandardScaler` to prepare the data for further analysis or ML models.\n")
        f.write("3. Raw and scaled datasets are saved as CSV files for reproducibility.\n\n")

        # CSVs
        f.write("### CSV Files\n")
        f.write(f"- Raw dataset: [`iris_raw.csv`](iris_raw.csv)\n")
        f.write(f"- Scaled dataset: [`iris_scaled.csv`](iris_scaled.csv)\n\n")

        f.write("## Exploratory Data Analysis (EDA)\n")
        f.write("EDA helps understand feature distributions, relationships, and potential outliers.\n\n")

        # Missing values
        f.write(f"### Missing Values Heatmap\n")
        f.write("Shows whether there are any missing values in the dataset. Light areas indicate missing values.\n")
        f.write(f"![Missing Values](iris_missing_values.png)\n\n")

        # Pairplots
        f.write(f"### Pairplot - Raw Data\n")
        f.write("Visualizes the pairwise relationships between features before scaling. Colors indicate species.\n")
        f.write(f"![Pairplot Raw](iris_pairplot_raw.png)\n\n")

        f.write(f"### Pairplot - Scaled Data\n")
        f.write("Pairplot after scaling numerical features, demonstrating that relationships between features are preserved.\n")
        f.write(f"![Pairplot Scaled](iris_pairplot_scaled.png)\n\n")

        # Correlation heatmap
        f.write(f"### Correlation Heatmap\n")
        f.write("Shows the Pearson correlation between numerical features. Strong positive/negative correlations are highlighted.\n")
        f.write(f"![Correlation Heatmap](iris_correlation_heatmap.png)\n\n")

        f.write("## Summary\n")
        f.write("- The dataset is clean with no missing values.\n")
        f.write("- Standardization was applied to numerical features.\n")
        f.write("- EDA plots reveal relationships between features and species.\n")
        f.write("- All preprocessing and EDA outputs are saved in this folder (`task1_output`) to meet Task 1 rubric requirements.\n")

    print(f"[INFO] Markdown report with explanations generated at {report_path}")
    return report_path
