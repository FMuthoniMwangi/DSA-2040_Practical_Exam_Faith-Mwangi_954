# data_mining/main.py
import preprocessing
import eda
import report

def main():
    # Step 1: Preprocess
    df_raw, df_scaled = preprocessing.run()

    # Step 2: EDA
    eda.run(df_raw, df_scaled)

    # Step 3: Generate Markdown report
    report.generate_md_report()

if __name__ == "__main__":
    main()
