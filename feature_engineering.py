
def create_features(df):
    df = df.copy()

    # 1. DTI Category
    def categorize_dti(dti):
        if dti < 0.30:
            return "LOW"
        elif dti < 0.50:
            return "MODERATE"
        else:
            return "HIGH"

    df["dti_category"] = df["debt_to_income"].apply(categorize_dti)

    # 2. Delinquency Category
    def categorize_delinquency(days):
        if days == 0:
            return "CURRENT"
        elif days <= 30:
            return "EARLY"
        elif days <= 90:
            return "LATE"
        else:
            return "SEVERE"

    df["delinquency_category"] = df["tunggakan_hari"].apply(
        categorize_delinquency
    )

    # 3. Credit Quality
    def categorize_credit_quality(kol):
        if kol == 1:
            return "GOOD"
        elif kol == 2:
            return "WATCH"
        else:
            return "BAD"

    df["credit_quality"] = df["kolektibilitas"].apply(
        categorize_credit_quality
    )

    return df
