def recommend_action(row):
    risk_level = row["risk_level"]
    dti_category = row["dti_category"]
    delinquency_category = row["delinquency_category"]
    credit_quality = row["credit_quality"]

    # HIGH RISK
    if risk_level == "HIGH":

        if delinquency_category == "SEVERE":
            return "Immediate Review & Collection Assessment"

        elif dti_category == "HIGH":
            return "Debt Capacity & Repayment Review"

        elif credit_quality == "BAD":
            return "Credit Quality Investigation"

        else:
            return "Intensive Risk Monitoring"

    # MEDIUM RISK
    elif risk_level == "MEDIUM":

        if delinquency_category in ["LATE", "EARLY"]:
            return "Payment Behavior Monitoring"

        elif dti_category == "HIGH":
            return "Financial Capacity Review"

        else:
            return "Periodic Credit Review"

    # LOW RISK
    elif risk_level == "LOW":

        if delinquency_category == "CURRENT":
            return "Routine Monitoring"

        else:
            return "Preventive Monitoring"

    return "Manual Assessment"