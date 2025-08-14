# data_mining/report.py
import os

# Output path
OUTPUT_DIR = os.path.join("data_exploration", "task1_output")

def generate_md_report():
    """Generate a Markdown report of preprocessing & EDA outputs."""
    report_path = os.path.join(OUTPUT_DIR, "report.md")

    with open(report_path, "w") as f:
        f.write("# Iris Dataset Preprocessing & EDA Report\n\n")
        f.write("This report summarizes the preprocessing and exploratory data analysis outputs.\n\n")

        # CSVs
        f.write("## CSV Files\n")
        f.write(f"- Raw dataset: [`iris_raw.csv`](iris_raw.csv)\n")
        f.write(f"- Scaled dataset: [`iris_scaled.csv`](iris_scaled.csv)\n\n")

        # Plots
        f.write("## Visualizations\n")
        f.write(f"### Missing Values Heatmap\n")
        f.write(f"![Missing Values](iris_missing_values.png)\n\n")

        f.write(f"### Pairplot - Raw Data\n")
        f.write(f"![Pairplot Raw](iris_pairplot_raw.png)\n\n")

        f.write(f"### Pairplot - Scaled Data\n")
        f.write(f"![Pairplot Scaled](iris_pairplot_scaled.png)\n\n")

        f.write(f"### Correlation Heatmap\n")
        f.write(f"![Correlation Heatmap](iris_correlation_heatmap.png)\n\n")

    print(f"[INFO] Markdown report generated at {report_path}")
    return report_path
