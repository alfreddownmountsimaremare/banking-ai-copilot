import pandas as pd

from feature_engineering import create_features
from src.risk_engine import analyze_credit_risk
from src.action_recommendation import recommend_action
from src.risk_explainer import explain_risk
from src.insight_generator import generate_portfolio_insights
from src.early_warning import assess_early_warning
from src.debtor_investigation import investigate_debtor


print("=" * 60)
print("BANKING AI COPILOT - ENGINE VALIDATION")
print("=" * 60)


# 1. LOAD DATA
df = pd.read_csv("data/sample/debtors.csv")

print("\n[1] DATA LOADING")
print("Total records:", len(df))


# 2. FEATURE ENGINEERING
df = create_features(df)

print("\n[2] FEATURE ENGINEERING")
print("Status: SUCCESS")
print("Generated columns:", list(df.columns))


# 3. RISK ENGINE
debtors = df.to_dict(orient="records")

results = analyze_credit_risk(debtors)

results_df = pd.DataFrame(results)

eda_df = df.merge(
    results_df,
    on="debtor_id"
)

print("\n[3] RISK ENGINE")
print("Status: SUCCESS")
print("Risk records:", len(results_df))


# 4. PORTFOLIO INSIGHTS
insights = generate_portfolio_insights(eda_df)

print("\n[4] PORTFOLIO INTELLIGENCE")
print("Status: SUCCESS")
print("Generated insights:", len(insights))


# 5. DEBTOR-LEVEL VALIDATION
if not eda_df.empty:

    row = eda_df.iloc[0]

    # Risk recommendation
    action = recommend_action(row)

    # Risk explanation
    explanation = explain_risk(row)

    # Early warning
    warning = assess_early_warning(row)

    # Debtor investigation
    investigation = investigate_debtor(row)

    print("\n[5] ACTION RECOMMENDATION")
    print("Status: SUCCESS")
    print("Recommendation:", action)

    print("\n[6] RISK EXPLAINER")
    print("Status: SUCCESS")
    print("Risk drivers:", explanation["risk_drivers"])

    print("\n[7] EARLY WARNING SYSTEM")
    print("Status: SUCCESS")
    print("Warning score:", warning["warning_score"])
    print("EWS level:", warning["ews_level"])

    print("\n[8] DEBTOR INVESTIGATION")
    print("Status: SUCCESS")
    print("Priority:", investigation["investigation_priority"])
    print("Condition:", investigation["debtor_condition"])

else:

    print("No debtor data available for engine validation.")


print("\n" + "=" * 60)
print("ENGINE VALIDATION COMPLETED")
print("=" * 60)