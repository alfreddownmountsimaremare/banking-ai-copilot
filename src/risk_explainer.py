def explain_risk(row):

    risk_drivers = []
    explanations = []

    # ==========================================
    # 1. DELINQUENCY ANALYSIS
    # ==========================================

    if row["tunggakan_hari"] > 90:

        risk_drivers.append("SEVERE DELINQUENCY")

        explanations.append(
            "Severe payment delinquency exceeding 90 days"
        )

    elif row["tunggakan_hari"] > 30:

        risk_drivers.append("LATE PAYMENT")

        explanations.append(
            "Payment delinquency exceeding 30 days"
        )

    elif row["tunggakan_hari"] > 0:

        risk_drivers.append("EARLY DELINQUENCY")

        explanations.append(
            "Early signs of payment delay"
        )

    # ==========================================
    # 2. DEBT-TO-INCOME ANALYSIS
    # ==========================================

    if row["debt_to_income"] >= 0.50:

        risk_drivers.append("HIGH DTI")

        explanations.append(
            "High debt burden relative to income"
        )

    elif row["debt_to_income"] >= 0.30:

        risk_drivers.append("MODERATE DTI")

        explanations.append(
            "Moderate debt burden relative to income"
        )

    # ==========================================
    # 3. CREDIT QUALITY ANALYSIS
    # ==========================================

    if row["credit_quality"] == "BAD":

        risk_drivers.append("BAD CREDIT QUALITY")

        explanations.append(
            "Debtor classified under poor credit quality"
        )

    elif row["credit_quality"] == "WATCH":

        risk_drivers.append("CREDIT WATCH")

        explanations.append(
            "Debtor requires additional monitoring"
        )

    # ==========================================
    # 4. RISK LEVEL
    # ==========================================

    if row["risk_level"] == "HIGH":

        overall_explanation = (
            "High risk profile requiring immediate review."
        )

    elif row["risk_level"] == "MEDIUM":

        overall_explanation = (
            "Moderate risk profile requiring further monitoring."
        )

    else:

        overall_explanation = (
            "Low risk profile under current assessment."
        )

    # ==========================================
    # 5. RETURN RESULT
    # ==========================================

    return {
        "risk_drivers": risk_drivers,
        "risk_explanation": (
            " | ".join(explanations)
            if explanations
            else "No significant risk drivers identified."
        ),
        "overall_explanation": overall_explanation
    }