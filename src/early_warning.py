
def assess_early_warning(row):

    warning_score = 0
    warning_indicators = []

    # ==========================================
    # 1. SEVERE DELINQUENCY
    # ==========================================

    tunggakan = row.get("tunggakan_hari", 0)

    if tunggakan > 90:

        warning_score += 35

        warning_indicators.append(
            "Severe Delinquency (>90 days)"
        )

    elif tunggakan > 30:

        warning_score += 20

        warning_indicators.append(
            "Late Payment (>30 days)"
        )


    # ==========================================
    # 2. HIGH DTI
    # ==========================================

    dti = row.get("debt_to_income", 0)

    if dti >= 0.50:

        warning_score += 20

        warning_indicators.append(
            "High Debt-to-Income Ratio"
        )


    # ==========================================
    # 3. BAD CREDIT QUALITY
    # ==========================================

    credit_quality = row.get("credit_quality", "")

    if credit_quality == "BAD":

        warning_score += 15

        warning_indicators.append(
            "Bad Credit Quality"
        )


    # ==========================================
    # 4. HIGH RISK CLASSIFICATION
    # ==========================================

    risk_level = row.get("risk_level", "")

    if risk_level == "HIGH":

        warning_score += 20

        warning_indicators.append(
            "High Risk Classification"
        )


    # ==========================================
    # 5. MULTIPLE WARNING BONUS
    # ==========================================

    number_of_warnings = len(warning_indicators)

    if number_of_warnings >= 3:

        warning_score += 10

        warning_indicators.append(
            "Multiple Risk Signals Detected"
        )


    # ==========================================
    # 6. EARLY WARNING LEVEL
    # ==========================================

    if warning_score >= 60:

        ews_level = "CRITICAL"

        monitoring_priority = "IMMEDIATE REVIEW"

    elif warning_score >= 40:

        ews_level = "HIGH"

        monitoring_priority = "INTENSIVE MONITORING"

    elif warning_score >= 20:

        ews_level = "MEDIUM"

        monitoring_priority = "PERIODIC REVIEW"

    else:

        ews_level = "LOW"

        monitoring_priority = "ROUTINE MONITORING"


    # ==========================================
    # 7. RETURN RESULTS
    # ==========================================

    return {
        "warning_score": warning_score,
        "ews_level": ews_level,
        "warning_indicators": warning_indicators,
        "monitoring_priority": monitoring_priority,
        "warning_count": number_of_warnings
    }
