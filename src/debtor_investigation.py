
def investigate_debtor(row):

    debtor_id = row.get("debtor_id", "UNKNOWN")

    risk_score = row.get("risk_score", 0)
    risk_level = row.get("risk_level", "UNKNOWN")

    dti = row.get("debt_to_income", 0)
    delinquency = row.get("tunggakan_hari", 0)

    credit_quality = row.get("credit_quality", "UNKNOWN")
    kolektibilitas = row.get("kolektibilitas", "UNKNOWN")

    ews_level = row.get("ews_level", "UNKNOWN")
    warning_score = row.get("warning_score", 0)

    risk_drivers = row.get("risk_drivers", [])
    warning_indicators = row.get("warning_indicators", [])

    recommended_action = row.get(
        "recommended_action",
        "No recommendation available"
    )

    # ==========================================
    # 1. FINANCIAL CAPACITY
    # ==========================================

    if dti >= 0.70:
        financial_condition = "VERY HIGH DEBT BURDEN"

    elif dti >= 0.50:
        financial_condition = "HIGH DEBT BURDEN"

    elif dti >= 0.30:
        financial_condition = "MODERATE DEBT BURDEN"

    else:
        financial_condition = "HEALTHY DEBT BURDEN"


    # ==========================================
    # 2. PAYMENT BEHAVIOR
    # ==========================================

    if delinquency > 90:
        payment_condition = "SEVERE DELINQUENCY"

    elif delinquency > 30:
        payment_condition = "HIGH DELINQUENCY"

    elif delinquency > 0:
        payment_condition = "EARLY DELINQUENCY"

    else:
        payment_condition = "CURRENT"


    # ==========================================
    # 3. CREDIT QUALITY ASSESSMENT
    # ==========================================

    if credit_quality == "BAD":
        credit_assessment = "POOR"

    elif credit_quality == "WATCH":
        credit_assessment = "NEEDS ATTENTION"

    elif credit_quality == "GOOD":
        credit_assessment = "HEALTHY"

    else:
        credit_assessment = "UNCLASSIFIED"


    # ==========================================
    # 4. RISK SIGNAL AGGREGATION
    # ==========================================

    risk_signals = []

    if dti >= 0.50:
        risk_signals.append(
            "High debt-to-income ratio"
        )

    if delinquency > 30:
        risk_signals.append(
            "Payment delinquency detected"
        )

    if credit_quality == "BAD":
        risk_signals.append(
            "Poor credit quality"
        )

    if risk_level == "HIGH":
        risk_signals.append(
            "High credit risk classification"
        )

    if ews_level in ["CRITICAL", "HIGH"]:
        risk_signals.append(
            f"{ews_level} early warning alert"
        )


    # ==========================================
    # 5. INVESTIGATION PRIORITY
    # ==========================================

    if ews_level == "CRITICAL":

        investigation_priority = "IMMEDIATE INVESTIGATION"

    elif ews_level == "HIGH":

        investigation_priority = "URGENT REVIEW"

    elif risk_level == "HIGH":

        investigation_priority = "INTENSIVE REVIEW"

    elif ews_level == "MEDIUM":

        investigation_priority = "PERIODIC INVESTIGATION"

    else:

        investigation_priority = "ROUTINE MONITORING"


    # ==========================================
    # 6. DEBTOR CONDITION SUMMARY
    # ==========================================

    if (
        risk_level == "HIGH"
        and delinquency > 30
        and dti >= 0.50
    ):

        debtor_condition = (
            "MULTIPLE RISK FACTORS — "
            "HIGH ATTENTION REQUIRED"
        )

    elif risk_level == "HIGH":

        debtor_condition = (
            "HIGH RISK — "
            "REQUIRES FURTHER REVIEW"
        )

    elif risk_level == "MEDIUM":

        debtor_condition = (
            "MODERATE RISK — "
            "CONTINUOUS MONITORING REQUIRED"
        )

    else:

        debtor_condition = (
            "LOW RISK — "
            "ROUTINE MONITORING"
        )


    # ==========================================
    # 7. INVESTIGATION OUTPUT
    # ==========================================

    return {

        "debtor_id": debtor_id,

        "risk_score": risk_score,

        "risk_level": risk_level,

        "financial_condition": financial_condition,

        "payment_condition": payment_condition,

        "credit_assessment": credit_assessment,

        "risk_signals": risk_signals,

        "investigation_priority": investigation_priority,

        "debtor_condition": debtor_condition,

        "ews_level": ews_level,

        "warning_score": warning_score,

        "risk_drivers": risk_drivers,

        "warning_indicators": warning_indicators,

        "kolektibilitas": kolektibilitas,

        "recommended_action": recommended_action

    }
