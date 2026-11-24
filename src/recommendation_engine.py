def generate_recommendations(eda_df):

    recommendations = []

    total_debtors = len(eda_df)

    if total_debtors == 0:
        print("No debtor data available.")
        return recommendations

    # ==========================================
    # 1. HIGH RISK PORTFOLIO
    # ==========================================

    high_risk_count = (
        eda_df["risk_level"] == "HIGH"
    ).sum()

    high_risk_ratio = (
        high_risk_count / total_debtors
    )

    if high_risk_ratio >= 0.30:

        recommendations.append({
            "priority": "HIGH",
            "category": "Portfolio Risk",
            "recommendation": (
                "Prioritize portfolio review and "
                "identify the main drivers of high risk."
            )
        })

    # ==========================================
    # 2. HIGH DTI
    # ==========================================

    high_dti_count = (
        eda_df["dti_category"] == "HIGH"
    ).sum()

    if high_dti_count > 0:

        recommendations.append({
            "priority": "MEDIUM",
            "category": "Debt Burden",
            "recommendation": (
                "Review borrowers with high debt-to-income "
                "ratios and evaluate repayment capacity."
            )
        })

    # ==========================================
    # 3. SEVERE DELINQUENCY
    # ==========================================

    severe_count = (
        eda_df["delinquency_category"] == "SEVERE"
    ).sum()

    if severe_count > 0:

        recommendations.append({
            "priority": "HIGH",
            "category": "Delinquency",
            "recommendation": (
                "Prioritize follow-up on severely overdue "
                "borrowers and assess recovery actions."
            )
        })

    # ==========================================
    # 4. BAD CREDIT QUALITY
    # ==========================================

    bad_quality_count = (
        eda_df["credit_quality"] == "BAD"
    ).sum()

    if bad_quality_count > 0:

        recommendations.append({
            "priority": "HIGH",
            "category": "Credit Quality",
            "recommendation": (
                "Conduct deeper credit reviews on borrowers "
                "classified as BAD."
            )
        })

    # ==========================================
    # 5. DATA QUALITY
    # ==========================================

    missing_values = (
        eda_df.isnull().sum().sum()
    )

    duplicate_ids = (
        eda_df["debtor_id"].duplicated().sum()
    )

    if missing_values > 0 or duplicate_ids > 0:

        recommendations.append({
            "priority": "MEDIUM",
            "category": "Data Quality",
            "recommendation": (
                "Resolve missing values and duplicate debtor "
                "records before relying on analytical results."
            )
        })

    # ==========================================
    # OUTPUT
    # ==========================================

    print("\n" + "=" * 65)
    print("             RISK RECOMMENDATION ENGINE")
    print("=" * 65)

    if len(recommendations) == 0:

        print("\nNo specific recommendations identified.")

    else:

        for i, item in enumerate(recommendations, start=1):

            print(f"\nRecommendation {i}")
            print(f"Priority   : {item['priority']}")
            print(f"Category  : {item['category']}")
            print(f"Action    : {item['recommendation']}")

    print("\nTotal Recommendations:", len(recommendations))
    print("=" * 65)

    return recommendations