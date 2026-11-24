
import pandas as pd


def analyze_risk_segments(df):
    print("\n" + "=" * 50)
    print("          RISK SEGMENT ANALYSIS")
    print("=" * 50)

    # 1. Risk level by credit quality
    print("\n--- RISK LEVEL BY CREDIT QUALITY ---")

    credit_quality_table = pd.crosstab(
        df["credit_quality"],
        df["risk_level"]
    )

    print(credit_quality_table)

    # 2. Risk level by DTI category
    print("\n--- RISK LEVEL BY DTI CATEGORY ---")

    dti_table = pd.crosstab(
        df["dti_category"],
        df["risk_level"]
    )

    print(dti_table)

    # 3. Risk level by delinquency category
    print("\n--- RISK LEVEL BY DELINQUENCY ---")

    delinquency_table = pd.crosstab(
        df["delinquency_category"],
        df["risk_level"]
    )

    print(delinquency_table)

    # 4. Average risk score by segment
    print("\n--- AVERAGE RISK SCORE BY DTI ---")

    average_score_by_dti = (
        df.groupby("dti_category")["risk_score"]
        .mean()
        .sort_values(ascending=False)
    )

    print(average_score_by_dti.round(2))

    print("\nRISK SEGMENT ANALYSIS COMPLETED")
    print("=" * 50)
