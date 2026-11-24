
import pandas as pd
from feature_engineering import create_features
from src.risk_engine import analyze_credit_risk
from src.risk_analysis import analyze_risk_segments
from src.insight_generator import generate_portfolio_insights
from src.recommendation_engine import generate_recommendations


# 1. Load dataset
df = pd.read_csv("data/sample/debtors.csv")
# Apply feature engineering
df = create_features(df)

print("\n--- FEATURE ENGINEERING RESULTS ---")

print(
    df[
        [
            "debtor_id",
            "debt_to_income",
            "dti_category",
            "tunggakan_hari",
            "delinquency_category",
            "kolektibilitas",
            "credit_quality"
        ]
    ].to_string(index=False)
)

# 2. Run credit risk engine
debtors = df.to_dict(orient="records")
results = analyze_credit_risk(debtors)

# 3. Convert analysis results into DataFrame
results_df = pd.DataFrame(results)

# 4. Portfolio statistics
total_debtors = len(df)

risk_distribution = (
    results_df["risk_level"]
    .value_counts()
    .reindex(["HIGH", "MEDIUM", "LOW"], fill_value=0)
)

high_risk_count = risk_distribution["HIGH"]
high_risk_percentage = (high_risk_count / total_debtors) * 100

average_dti = df["debt_to_income"].mean()
average_risk_score = results_df["risk_score"].mean()

overdue_debtors = (df["tunggakan_hari"] > 30).sum()

# 5. Display portfolio report
print("=" * 40)
print("       BANKING AI COPILOT")
print("       PORTFOLIO RISK REPORT")
print("=" * 40)

print(f"Total Debtors       : {total_debtors}")
print(f"High Risk Debtors   : {high_risk_count}")
print(f"High Risk Ratio     : {high_risk_percentage:.2f}%")
print(f"Average DTI         : {average_dti:.2%}")
print(f"Average Risk Score  : {average_risk_score:.2f}")
print(f"Overdue > 30 Days  : {overdue_debtors}")

print("\n--- RISK DISTRIBUTION ---")

for risk_level, count in risk_distribution.items():
    percentage = (count / total_debtors) * 100

    print(
        f"{risk_level:<10}: "
        f"{count:>3} debtors "
        f"({percentage:.2f}%)"
    )

print("=" * 40)


import matplotlib.pyplot as plt

# ==========================================
# 6. RISK DISTRIBUTION VISUALIZATION
# ==========================================

plt.figure(figsize=(8, 5))

risk_distribution.plot(kind="bar")

plt.title("Credit Risk Distribution")
plt.xlabel("Risk Level")
plt.ylabel("Number of Debtors")
plt.xticks(rotation=0)
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("charts/risk_distribution.png", dpi=300)
plt.show()


# ==========================================
# 7. DTI vs RISK SCORE
# ==========================================

risk_analysis_df = df.merge(
    results_df,
    on="debtor_id"
)

plt.figure(figsize=(8, 5))

for risk_level in ["LOW", "MEDIUM", "HIGH"]:
    subset = risk_analysis_df[
        risk_analysis_df["risk_level"] == risk_level
    ]

    plt.scatter(
        subset["debt_to_income"],
        subset["risk_score"],
        label=risk_level,
        s=80
    )

plt.title("Debt-to-Income vs Credit Risk Score")
plt.xlabel("Debt-to-Income Ratio")
plt.ylabel("Risk Score")
plt.legend(title="Risk Level")
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig("charts/dti_vs_risk_score.png", dpi=300)
plt.show()

print("COLUMNS DF:")
print(df.columns.tolist())

print("\nCOLUMNS RESULTS_DF:")
print(results_df.columns.tolist())

# ==========================================
# 8. EXPLORATORY DATA ANALYSIS (EDA)
# ==========================================

# Merge original data with risk analysis results
eda_df = df.merge(results_df, on="debtor_id")
# Run risk segment analysis
analyze_risk_segments(eda_df)

print("\n" + "=" * 50)
print("         EXPLORATORY DATA ANALYSIS")
print("=" * 50)

# 1. Dataset overview
print("\n--- DATASET OVERVIEW ---")
print(f"Total rows       : {eda_df.shape[0]}")
print(f"Total columns    : {eda_df.shape[1]}")
print(f"Duplicate debtors: {eda_df['debtor_id'].duplicated().sum()}")
print(f"Missing values   : {eda_df.isnull().sum().sum()}")

# 2. Column information
print("\n--- COLUMN INFORMATION ---")
print(eda_df.dtypes)

# 3. Statistical summary
print("\n--- STATISTICAL SUMMARY ---")
print(eda_df.describe().round(2))

# 4. Risk analysis
print("\n--- RISK ANALYSIS ---")
print(eda_df.groupby("risk_level").size())

# 5. Average DTI by risk level
print("\n--- AVERAGE DTI BY RISK ---")
print(
    eda_df.groupby("risk_level")["debt_to_income"]
    .mean()
    .round(2)
)

# 6. Missing value analysis
print("\n--- MISSING VALUE ANALYSIS ---")
print(eda_df.isnull().sum())

print("\nEDA COMPLETED")
print("=" * 50)


# ==========================================
# AUTOMATED PORTFOLIO INSIGHTS
# ==========================================

generate_portfolio_insights(eda_df)

# ==========================================
# RISK RECOMMENDATION ENGINE
# ==========================================

recommendations = generate_recommendations(eda_df)