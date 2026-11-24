def generate_portfolio_insights(eda_df):

    total_debtors = len(eda_df)

    insights = []

    if total_debtors == 0:
        return [
            {
                "category": "PORTFOLIO",
                "severity": "INFO",
                "title": "Empty Portfolio",
                "message": "No debtor data available for analysis."
            }
        ]

    # ==========================================
    # 1. HIGH RISK CONCENTRATION
    # ==========================================

    high_risk_count = (
        eda_df["risk_level"] == "HIGH"
    ).sum()

    high_risk_percentage = (
        high_risk_count / total_debtors * 100
    )

    if high_risk_percentage >= 40:
        severity = "CRITICAL"
        message = (
            f"{high_risk_percentage:.1f}% of the portfolio "
            f"({high_risk_count} debtors) is classified as HIGH risk. "
            "Immediate portfolio review is recommended."
        )

    elif high_risk_percentage >= 20:
        severity = "WARNING"
        message = (
            f"{high_risk_percentage:.1f}% of the portfolio "
            f"({high_risk_count} debtors) is classified as HIGH risk. "
            "Enhanced monitoring is recommended."
        )

    else:
        severity = "INFO"
        message = (
            f"{high_risk_percentage:.1f}% of the portfolio "
            f"({high_risk_count} debtors) is classified as HIGH risk."
        )

    insights.append({
        "category": "PORTFOLIO RISK",
        "severity": severity,
        "title": "High Risk Concentration",
        "message": message
    })


    # ==========================================
    # 2. HIGH DTI ANALYSIS
    # ==========================================

    high_dti_df = eda_df[
        eda_df["dti_category"] == "HIGH"
    ]

    high_dti_count = len(high_dti_df)

    high_dti_percentage = (
        high_dti_count / total_debtors * 100
    )

    high_dti_avg_score = (
        high_dti_df["risk_score"].mean()
        if high_dti_count > 0
        else 0
    )

    if high_dti_count > 0:

        if high_dti_avg_score >= 50:
            severity = "CRITICAL"

        elif high_dti_avg_score >= 30:
            severity = "WARNING"

        else:
            severity = "INFO"

        message = (
            f"{high_dti_count} debtors ({high_dti_percentage:.1f}% "
            f"of portfolio) belong to the HIGH DTI segment, "
            f"with an average risk score of {high_dti_avg_score:.2f}. "
            "Review repayment capacity and debt burden."
        )

    else:

        severity = "INFO"

        message = (
            "No debtors are currently classified in the HIGH DTI segment."
        )

    insights.append({
        "category": "FINANCIAL CAPACITY",
        "severity": severity,
        "title": "High Debt-to-Income",
        "message": message
    })


    # ==========================================
    # 3. SEVERE DELINQUENCY
    # ==========================================

    severe_df = eda_df[
        eda_df["delinquency_category"] == "SEVERE"
    ]

    severe_count = len(severe_df)

    severe_high_risk = (
        (severe_df["risk_level"] == "HIGH").sum()
    )

    severe_percentage = (
        severe_count / total_debtors * 100
    )

    if severe_count > 0:

        severity = (
            "CRITICAL"
            if severe_high_risk > 0
            else "WARNING"
        )

        message = (
            f"{severe_count} debtors ({severe_percentage:.1f}% "
            f"of portfolio) have SEVERE delinquency. "
            f"{severe_high_risk} of them are also classified as HIGH risk. "
            "Prioritize delinquency assessment and collection follow-up."
        )

    else:

        severity = "INFO"

        message = (
            "No debtors are currently classified under SEVERE delinquency."
        )

    insights.append({
        "category": "DELINQUENCY",
        "severity": severity,
        "title": "Severe Payment Delinquency",
        "message": message
    })


    # ==========================================
    # 4. BAD CREDIT QUALITY
    # ==========================================

    bad_quality_df = eda_df[
        eda_df["credit_quality"] == "BAD"
    ]

    bad_total = len(bad_quality_df)

    bad_high_risk = (
        (bad_quality_df["risk_level"] == "HIGH").sum()
    )

    bad_high_risk_percentage = (
        bad_high_risk / bad_total * 100
        if bad_total > 0
        else 0
    )

    if bad_total > 0:

        severity = (
            "CRITICAL"
            if bad_high_risk_percentage >= 70
            else "WARNING"
        )

        message = (
            f"{bad_high_risk} out of {bad_total} debtors with BAD "
            f"credit quality ({bad_high_risk_percentage:.1f}%) "
            f"are classified as HIGH risk. "
            "Further credit quality assessment is recommended."
        )

    else:

        severity = "INFO"

        message = (
            "No debtors are currently classified under BAD credit quality."
        )

    insights.append({
        "category": "CREDIT QUALITY",
        "severity": severity,
        "title": "Bad Credit Quality Exposure",
        "message": message
    })


    # ==========================================
    # 5. DATA QUALITY
    # ==========================================

    missing_values = (
        eda_df.isnull().sum().sum()
    )

    duplicate_debtors = (
        eda_df["debtor_id"].duplicated().sum()
    )

    if missing_values > 0 or duplicate_debtors > 0:

        severity = "WARNING"

        message = (
            f"Data quality issues detected. "
            f"Missing values: {missing_values}. "
            f"Duplicate debtor IDs: {duplicate_debtors}. "
            "Data validation is recommended before analysis."
        )

    else:

        severity = "INFO"

        message = (
            "No missing values or duplicate debtor IDs "
            "were detected in the current dataset."
        )

    insights.append({
        "category": "DATA QUALITY",
        "severity": severity,
        "title": "Data Quality Assessment",
        "message": message
    })


    # ==========================================
    # 6. PORTFOLIO SUMMARY
    # ==========================================

    medium_risk_count = (
        eda_df["risk_level"] == "MEDIUM"
    ).sum()

    low_risk_count = (
        eda_df["risk_level"] == "LOW"
    ).sum()

    insights.append({
        "category": "PORTFOLIO SUMMARY",
        "severity": "INFO",
        "title": "Portfolio Composition",
        "message": (
            f"Portfolio consists of {total_debtors} debtors: "
            f"{high_risk_count} HIGH risk, "
            f"{medium_risk_count} MEDIUM risk, and "
            f"{low_risk_count} LOW risk."
        )
    })


    # ==========================================
    # 7. RETURN INSIGHTS
    # ==========================================

    return insights