
def analyze_credit_risk(debtors):
    results = []

    for debtor in debtors:
        score = 0
        risk_factors = []

        # Kolektibilitas
        if debtor["kolektibilitas"] >= 3:
            score += 40
            risk_factors.append("Poor collectibility")
        elif debtor["kolektibilitas"] == 2:
            score += 20
            risk_factors.append("Special mention")

        # Tunggakan
        if debtor["tunggakan_hari"] > 90:
            score += 30
            risk_factors.append("Severe delinquency")
        elif debtor["tunggakan_hari"] > 30:
            score += 15
            risk_factors.append("Payment overdue")

        # Debt-to-income
        if debtor["debt_to_income"] > 0.70:
            score += 30
            risk_factors.append("High debt-to-income ratio")
        elif debtor["debt_to_income"] > 0.40:
            score += 15
            risk_factors.append("Elevated debt-to-income ratio")

        # Risk classification
        if score >= 60:
            risk_level = "HIGH"
        elif score >= 30:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        results.append({
            "debtor_id": debtor["debtor_id"],
            "risk_score": score,
            "risk_level": risk_level,
            "risk_factors": risk_factors
        })

    return results
