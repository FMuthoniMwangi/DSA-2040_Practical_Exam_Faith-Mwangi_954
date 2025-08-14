import os

# Paths to individual reports
TASK1_REPORT = "data_mining/task1_output/iris_report.md"
TASK2_REPORT = "data_mining/clustering/task2_output/iris_clustering_report.md"
TASK3_REPORT = "data_mining/classification/task3_output/iris_task3_report.md"
DW_DESIGN_REPORT = "data_warehousing/design/design_report.md"
DW_OLAP_REPORT = "data_warehousing/olap/olap_report.md"

# Save ultimate report in the top-level project folder
ULTIMATE_REPORT_PATH = "DSA_2040_ultimate_report.md"


def combine_reports():
    """Combine all individual task reports into one ultimate report."""
    with open(ULTIMATE_REPORT_PATH, "w") as out_file:
        out_file.write("# Ultimate Exam Report: DSA 2040\n\n")
        out_file.write("This report consolidates all tasks from Data Warehousing and Data Mining.\n\n")

        # Data Warehousing: Design
        if os.path.exists(DW_DESIGN_REPORT):
            with open(DW_DESIGN_REPORT, "r") as f:
                out_file.write("## Data Warehousing: Task 1 – Design\n\n")
                out_file.write(f.read() + "\n\n")
        else:
            out_file.write("## Data Warehousing: Task 1 – Design\n\nReport not found.\n\n")

        # Data Warehousing: OLAP
        if os.path.exists(DW_OLAP_REPORT):
            with open(DW_OLAP_REPORT, "r") as f:
                out_file.write("## Data Warehousing: Task 2 – OLAP Queries & Analysis\n\n")
                out_file.write(f.read() + "\n\n")
        else:
            out_file.write("## Data Warehousing: Task 2 – OLAP Queries & Analysis\n\nReport not found.\n\n")

        # Data Mining: Preprocessing & EDA
        if os.path.exists(TASK1_REPORT):
            with open(TASK1_REPORT, "r") as f:
                out_file.write("## Data Mining: Task 1 – Preprocessing & EDA\n\n")
                out_file.write(f.read() + "\n\n")
        else:
            out_file.write("## Data Mining: Task 1 – Preprocessing & EDA\n\nReport not found.\n\n")

        # Data Mining: Clustering
        if os.path.exists(TASK2_REPORT):
            with open(TASK2_REPORT, "r") as f:
                out_file.write("## Data Mining: Task 2 – Clustering\n\n")
                out_file.write(f.read() + "\n\n")
        else:
            out_file.write("## Data Mining: Task 2 – Clustering\n\nReport not found.\n\n")

        # Data Mining: Classification & Association Rules
        if os.path.exists(TASK3_REPORT):
            with open(TASK3_REPORT, "r") as f:
                out_file.write("## Data Mining: Task 3 – Classification & Association Rule Mining\n\n")
                out_file.write(f.read() + "\n\n")
        else:
            out_file.write("## Data Mining: Task 3 – Classification & Association Rule Mining\n\nReport not found.\n\n")

    print(f"[INFO] Ultimate report generated at {ULTIMATE_REPORT_PATH}")
    return ULTIMATE_REPORT_PATH


if __name__ == "__main__":
    combine_reports()
