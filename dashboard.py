
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from html import escape

from src.risk_engine import analyze_credit_risk
from feature_engineering import create_features
from src.action_recommendation import recommend_action
from src.risk_explainer import explain_risk
from src.insight_generator import generate_portfolio_insights
from src.early_warning import assess_early_warning
from src.debtor_investigation import investigate_debtor


# =========================================================
# 1. CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Banking AI Copilot",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# 2. DESIGN SYSTEM
# =========================================================

st.markdown("""
<style>
:root {
    --navy: #102A43;
    --blue: #246BFD;
    --bg: #F3F6FA;
    --text: #24364B;
    --muted: #718096;
    --border: #E5EAF1;
    --green: #20A779;
    --yellow: #E6B344;
    --orange: #F09543;
    --red: #E65B68;
}

.stApp {
    background: var(--bg);
    color: var(--text);
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 1rem !important;
    max-width: 1600px;
}

h1, h2, h3 {
    color: var(--navy) !important;
}

p {
    color: var(--muted);
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #102A43;
}

section[data-testid="stSidebar"] * {
    color: #EAF1FA;
}

section[data-testid="stSidebar"] [data-testid="stRadio"] label {
    padding: 9px 12px;
    border-radius: 10px;
    margin-bottom: 4px;
}

section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: #1E4265;
}

section[data-testid="stSidebar"] [data-testid="stRadio"] p {
    color: #EAF1FA !important;
    font-weight: 600;
}

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 4px 24px 4px;
}

.brand-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 42px;
    height: 42px;
    border-radius: 13px;
    background: #246BFD;
    color: white;
    font-size: 23px;
    font-weight: 700;
}

.sidebar-brand b {
    display: block;
    font-size: 16px;
    color: white;
}

.sidebar-brand small {
    display: block;
    font-size: 9px;
    letter-spacing: 1.4px;
    color: #A9C3DF;
    margin-top: 3px;
}

.sidebar-section-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #7898B9;
    margin: 10px 0;
}

.sidebar-bottom {
    margin-top: 24px;
    padding: 14px;
    border: 1px solid #31516F;
    border-radius: 12px;
    color: #BBD0E7;
    font-size: 10px;
}

.sidebar-bottom small {
    display: block;
    color: #A9C3DF;
    margin-top: 5px;
}

.status-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    background: #34C98A;
    border-radius: 50%;
    margin-right: 6px;
}

/* HEADER */

.page-heading {
    margin-bottom: 8px;
}

.page-eyebrow {
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 1.7px;
    color: #5280B8;
    margin-bottom: 4px;
}

.page-heading h1 {
    font-size: 26px;
    font-weight: 750;
    letter-spacing: -0.8px;
    margin: 0;
    color: #102A43;
}

.page-heading p {
    font-size: 11px;
    margin: 3px 0 10px 0;
}

/* FILTERS */

.filter-label {
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 1px;
    color: #718096;
    margin-bottom: 5px;
}

div[data-testid="stSelectbox"] label {
    font-size: 10px !important;
    font-weight: 600 !important;
    color: #718096 !important;
}

div[data-testid="stSelectbox"] > div > div {
    border-radius: 9px !important;
    min-height: 34px;
    background: white;
}

div[data-testid="stButton"] button {
    border-radius: 9px;
    min-height: 36px;
    font-weight: 600;
    font-size: 11px;
}

/* CARDS */

[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #E5EAF1 !important;
    border-radius: 13px !important;
    background: white;
}

.custom-card {
    background: white;
    border: 1px solid #E5EAF1;
    border-radius: 14px;
    padding: 14px;
    box-shadow: 0 2px 8px rgba(25, 52, 82, 0.035);
    margin-bottom: 8px;
}

.card-heading {
    margin-bottom: 9px;
}

.card-heading b {
    display: block;
    font-size: 12px;
    font-weight: 700;
    color: #20364D;
}

.card-heading small {
    display: block;
    font-size: 9px;
    color: #8593A5;
    margin-top: 2px;
}

.section-title {
    font-size: 12px;
    font-weight: 750;
    color: #20364D;
    margin: 10px 0 8px 0;
}

/* KPI */

.kpi-top {
    display: flex;
    align-items: center;
    gap: 8px;
}

.kpi-icon {
    width: 30px;
    height: 30px;
    border-radius: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    font-weight: 700;
}

.kpi-icon.blue {
    background: #EAF2FF;
    color: #246BFD;
}

.kpi-icon.red {
    background: #FFF0F1;
    color: #E65B68;
}

.kpi-icon.purple {
    background: #F1ECFF;
    color: #8664D8;
}

.kpi-icon.teal {
    background: #E8F8F4;
    color: #20A779;
}

.kpi-label {
    color: #78879A;
    font-size: 10px;
    font-weight: 600;
}

.kpi-value {
    font-size: 25px;
    font-weight: 750;
    color: #102A43;
    letter-spacing: -0.7px;
    margin-top: 7px;
    line-height: 1.1;
}

.kpi-note {
    font-size: 9px;
    color: #8A98A9;
    margin-top: 5px;
}

/* ALERTS */

.alert-row {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 9px;
    border-radius: 10px;
    margin-bottom: 6px;
    border: 1px solid transparent;
}

.alert-row.critical {
    background: #FFF1F2;
    border-color: #FBE0E3;
}

.alert-row.high {
    background: #FFF5EA;
    border-color: #F8E5CD;
}

.alert-row.medium {
    background: #FFFAEB;
    border-color: #F5EBCB;
}

.alert-row.low {
    background: #EAF8F1;
    border-color: #D6EFE3;
}

.alert-icon {
    width: 27px;
    height: 27px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 700;
}

.critical .alert-icon {
    background: #FFE0E4;
    color: #D94354;
}

.high .alert-icon {
    background: #FFE9D0;
    color: #D78029;
}

.medium .alert-icon {
    background: #FFF0C6;
    color: #B28B26;
}

.low .alert-icon {
    background: #D8F1E4;
    color: #23966B;
}

.alert-name {
    flex: 1;
    font-size: 9px;
    font-weight: 700;
}

.critical .alert-name { color: #C84251; }
.high .alert-name { color: #CA7925; }
.medium .alert-name { color: #B28B26; }
.low .alert-name { color: #23966B; }

.alert-row b {
    font-size: 15px;
    color: #20364D;
}

.alert-foot {
    font-size: 9px;
    color: #75869B;
    padding-top: 5px;
}

/* INSIGHTS */

.insight-item {
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 7px;
    border: 1px solid transparent;
}

.insight-critical {
    background: #FFF1F2;
    border-color: #F8D9DE;
}

.insight-warning {
    background: #FFF7EA;
    border-color: #F4E1C6;
}

.insight-info {
    background: #EFF5FF;
    border-color: #DFEAFE;
}

.insight-tag {
    display: inline-block;
    font-size: 8px;
    font-weight: 750;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
}

.insight-critical .insight-tag { color: #D44958; }
.insight-warning .insight-tag { color: #C8832D; }
.insight-info .insight-tag { color: #4679C7; }

.insight-item b {
    display: block;
    color: #263B53;
    font-size: 10px;
    line-height: 1.35;
}

.insight-item p {
    font-size: 9px;
    color: #6F8196;
    margin: 4px 0 0 0;
    line-height: 1.45;
}

/* DETAILS */

.detail-box {
    background: #F7F9FC;
    border: 1px solid #E8EDF4;
    border-radius: 10px;
    padding: 11px;
    min-height: 78px;
    margin-bottom: 8px;
}

.detail-label {
    color: #8291A4;
    font-size: 9px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.4px;
    margin-bottom: 5px;
}

.detail-value {
    color: #20364D;
    font-size: 12px;
    font-weight: 650;
    line-height: 1.4;
    overflow-wrap: anywhere;
}

.detail-description {
    color: #708198;
    font-size: 10px;
    line-height: 1.5;
    margin-top: 5px;
}

.explanation-box {
    background: white;
    border: 1px solid #E5EAF1;
    border-radius: 12px;
    padding: 13px;
    margin-bottom: 8px;
}

.explanation-box p {
    font-size: 10px;
    color: #667A91;
    line-height: 1.55;
    margin: 0;
}

.driver-chip {
    display: inline-block;
    padding: 5px 8px;
    margin: 3px 4px 3px 0;
    border-radius: 7px;
    background: #EFF5FF;
    color: #3569B8;
    border: 1px solid #DCE9FC;
    font-size: 9px;
    font-weight: 600;
}

/* EMPTY STATE */

.empty-state {
    text-align: center;
    padding: 25px 10px;
    color: #8B9AAD;
    font-size: 10px;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #E7ECF3;
    border-radius: 12px;
    overflow: hidden;
}

@media (max-width: 1100px) {
    .kpi-value {
        font-size: 20px;
    }
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. GENERAL HELPER FUNCTIONS
# =========================================================

def safe_text(value, default="-"):
    if value is None:
        return default

    try:
        if pd.isna(value):
            return default
    except (TypeError, ValueError):
        pass

    return str(value)


def safe_float(value, default=0.0):
    try:
        if value is None or pd.isna(value):
            return default

        return float(value)

    except (TypeError, ValueError):
        return default


def normalize_dict(value):
    if isinstance(value, dict):
        return value

    return {}


def normalize_level(value, allowed):
    value = safe_text(value, "LOW").upper()

    if value not in allowed:
        return "LOW"

    return value


def card_title(title, subtitle=""):
    st.markdown(
        f"""
        <div class="card-heading">
            <b>{escape(str(title))}</b>
            <small>{escape(str(subtitle))}</small>
        </div>
        """,
        unsafe_allow_html=True
    )


def html_card(content):
    st.markdown(
        f'<div class="custom-card">{content}</div>',
        unsafe_allow_html=True
    )


def kpi(label, value, note, icon, color_class):
    html_card(f"""
        <div class="kpi-top">
            <span class="kpi-icon {color_class}">{icon}</span>
            <span class="kpi-label">{escape(str(label))}</span>
        </div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-note">{escape(str(note))}</div>
    """)


def show_empty(message="No data available"):
    st.markdown(
        f"<div class='empty-state'>{escape(message)}</div>",
        unsafe_allow_html=True
    )


def render_detail_box(label, value, description=""):
    st.markdown(f"""
        <div class="detail-box">
            <div class="detail-label">{escape(str(label))}</div>
            <div class="detail-value">{escape(str(value))}</div>
            <div class="detail-description">{escape(str(description))}</div>
        </div>
    """, unsafe_allow_html=True)


def format_explanation_value(value):
    if value is None:
        return "-"

    if isinstance(value, (list, tuple, set)):
        return ", ".join(map(str, value))

    if isinstance(value, dict):
        return "; ".join(
            f"{key}: {val}"
            for key, val in value.items()
        )

    return str(value)


def render_dataframe(data, height=350, column_config=None):
    if data is None or data.empty:
        show_empty()
        return

    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True,
        height=height,
        column_config=column_config
    )


# =========================================================
# 4. CHART FUNCTIONS
# =========================================================

def chart_layout(height=180):
    return dict(
        height=height,
        margin=dict(l=8, r=18, t=12, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Arial",
            color="#64758B",
            size=10
        )
    )


def make_bar_chart(labels, values, colors, height=175):
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=list(labels),
            y=list(values),
            marker=dict(
                color=colors,
                line=dict(width=0)
            ),
            text=list(values),
            textposition="outside",
            textfont=dict(size=10, color="#52657B"),
            width=0.48
        )
    )

    fig.update_layout(
        **chart_layout(height),
        showlegend=False,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            tickfont=dict(size=9, color="#77879B")
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#EDF1F6",
            zeroline=False,
            tickfont=dict(size=9, color="#77879B"),
            rangemode="tozero"
        ),
        bargap=0.38
    )

    return fig


def make_horizontal_chart(labels, values, colors, height=170):
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=list(labels),
            x=list(values),
            orientation="h",
            marker=dict(
                color=colors,
                line=dict(width=0)
            ),
            text=list(values),
            textposition="outside",
            textfont=dict(size=10, color="#52657B")
        )
    )

    fig.update_layout(
        **chart_layout(height),
        showlegend=False,
        xaxis=dict(
            showgrid=True,
            gridcolor="#EDF1F6",
            zeroline=False,
            tickfont=dict(size=8),
            rangemode="tozero"
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            tickfont=dict(size=9, color="#64758B"),
            autorange="reversed"
        ),
        bargap=0.38
    )

    return fig


def show_chart(fig):
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True
        }
    )


# =========================================================
# 5. LOAD AND PREPARE DATA
# =========================================================

@st.cache_data(show_spinner="Loading portfolio data...")
def load_data():

    df = pd.read_csv("data/sample/debtors.csv")

    if df.empty:
        raise ValueError("Dataset debtors.csv tidak memiliki data.")

    # Feature engineering
    df = create_features(df)

    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            "create_features() harus mengembalikan pandas DataFrame."
        )

    if "debtor_id" not in df.columns:
        raise ValueError(
            "Kolom debtor_id tidak ditemukan dalam dataset."
        )

    # Risk engine
    risk_result = analyze_credit_risk(
        df.to_dict(orient="records")
    )

    if isinstance(risk_result, pd.DataFrame):
        results_df = risk_result.copy()

    elif isinstance(risk_result, list):
        results_df = pd.DataFrame(risk_result)

    else:
        raise TypeError(
            "analyze_credit_risk() harus mengembalikan list atau DataFrame."
        )

    if results_df.empty:
        raise ValueError(
            "Risk engine tidak menghasilkan data penilaian risiko."
        )

    # Merge risk results
    if "debtor_id" in results_df.columns:

        if "risk_score" in df.columns and "risk_score" in results_df.columns:
            df = df.drop(columns=["risk_score"])

        if "risk_level" in df.columns and "risk_level" in results_df.columns:
            df = df.drop(columns=["risk_level"])

        df = df.merge(
            results_df,
            on="debtor_id",
            how="left",
            suffixes=("", "_risk")
        )

    else:
        if len(results_df) != len(df):
            raise ValueError(
                "Hasil risk engine tidak memiliki debtor_id dan jumlah "
                "barisnya berbeda dari dataset."
            )

        for column in results_df.columns:
            if column not in df.columns:
                df[column] = results_df[column].values

    # Pastikan kolom utama tersedia
    required_defaults = {
        "risk_score": 0,
        "risk_level": "LOW",
        "credit_quality": "WATCH",
        "dti_category": "LOW",
        "debt_to_income": 0,
        "kolektibilitas": "-",
        "tunggakan_hari": 0,
        "delinquency_category": "CURRENT"
    }

    for column, default_value in required_defaults.items():
        if column not in df.columns:
            df[column] = default_value

    df["risk_score"] = pd.to_numeric(
        df["risk_score"],
        errors="coerce"
    ).fillna(0)

    df["debt_to_income"] = pd.to_numeric(
        df["debt_to_income"],
        errors="coerce"
    ).fillna(0)

    df["tunggakan_hari"] = pd.to_numeric(
        df["tunggakan_hari"],
        errors="coerce"
    ).fillna(0)

    df["risk_level"] = (
        df["risk_level"]
        .astype(str)
        .str.upper()
    )

    df["credit_quality"] = (
        df["credit_quality"]
        .astype(str)
        .str.upper()
    )

    df["dti_category"] = (
        df["dti_category"]
        .astype(str)
        .str.upper()
    )

    return df


try:
    eda_df = load_data()

except Exception as error:
    st.error(f"Gagal memuat data: {error}")
    st.stop()


# =========================================================
# 6. SIDEBAR NAVIGATION
# =========================================================

pages = [
    "Overview",
    "Risk Analytics",
    "Early Warning",
    "Debtor Intelligence",
    "Action Center"
]

page_icons = {
    "Overview": "▦",
    "Risk Analytics": "◈",
    "Early Warning": "⚠",
    "Debtor Intelligence": "⌕",
    "Action Center": "↗"
}

with st.sidebar:

    st.markdown("""
    <div class="sidebar-brand">
        <span class="brand-icon">✦</span>
        <div>
            <b>Banking AI</b>
            <small>RISK INTELLIGENCE</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<div class='sidebar-section-label'>WORKSPACE</div>",
        unsafe_allow_html=True
    )

    page = st.radio(
        "Workspace",
        pages,
        format_func=lambda x: f"{page_icons[x]}   {x}",
        label_visibility="collapsed",
        key="main_navigation"
    )

    st.markdown("""
    <div class="sidebar-bottom">
        <span class="status-dot"></span>
        SYSTEM ACTIVE
        <small>Credit risk monitoring</small>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# 7. PAGE HEADER
# =========================================================

page_descriptions = {
    "Overview": (
        "Portfolio health, risk distribution, warning signals, "
        "and priority debtors."
    ),
    "Risk Analytics": (
        "Analyze portfolio risk, credit quality, debt burden, "
        "and risk distribution."
    ),
    "Early Warning": (
        "Monitor warning signals and borrowers requiring attention."
    ),
    "Debtor Intelligence": (
        "Investigate borrower profiles, risk factors, and recommendations."
    ),
    "Action Center": (
        "Prioritize follow-up activities and recommended actions."
    )
}

st.markdown(f"""
<div class="page-heading">
    <div class="page-eyebrow">
        CREDIT RISK & PORTFOLIO INTELLIGENCE
    </div>
    <h1>{escape(page)}</h1>
    <p>{escape(page_descriptions[page])}</p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# 8. FILTERS
# =========================================================

def reset_filters():
    st.session_state["filter_risk"] = "All"
    st.session_state["filter_quality"] = "All"
    st.session_state["filter_dti"] = "All"
    st.session_state["filter_kol"] = "All"


risk_options = ["All", "HIGH", "MEDIUM", "LOW"]

quality_options = [
    "All",
    "GOOD",
    "WATCH",
    "BAD"
]

dti_options = [
    "All",
    "LOW",
    "MODERATE",
    "HIGH"
]

kol_values = (
    eda_df["kolektibilitas"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

kol_options = ["All"] + sorted(kol_values)

# Pastikan nilai session state masih tersedia dalam options
for key, options in [
    ("filter_risk", risk_options),
    ("filter_quality", quality_options),
    ("filter_dti", dti_options),
    ("filter_kol", kol_options)
]:
    if key not in st.session_state:
        st.session_state[key] = "All"

    elif st.session_state[key] not in options:
        st.session_state[key] = "All"


st.markdown(
    "<div class='filter-label'>PORTFOLIO FILTERS</div>",
    unsafe_allow_html=True
)

f1, f2, f3, f4, f5 = st.columns(
    [1, 1, 1, 1, 0.72],
    gap="small"
)

with f1:
    selected_risk = st.selectbox(
        "Risk Level",
        risk_options,
        key="filter_risk"
    )

with f2:
    selected_quality = st.selectbox(
        "Credit Quality",
        quality_options,
        key="filter_quality"
    )

with f3:
    selected_dti = st.selectbox(
        "DTI Category",
        dti_options,
        key="filter_dti"
    )

with f4:
    selected_kol = st.selectbox(
        "Kolektibilitas",
        kol_options,
        key="filter_kol"
    )

with f5:
    st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)

    st.button(
        "↺ Reset Filter",
        use_container_width=True,
        on_click=reset_filters,
        key="reset_filter_button"
    )


# =========================================================
# 9. APPLY FILTERS
# =========================================================

filtered_df = eda_df.copy()

if selected_risk != "All":
    filtered_df = filtered_df[
        filtered_df["risk_level"] == selected_risk
    ]

if selected_quality != "All":
    filtered_df = filtered_df[
        filtered_df["credit_quality"] == selected_quality
    ]

if selected_dti != "All":
    filtered_df = filtered_df[
        filtered_df["dti_category"] == selected_dti
    ]

if selected_kol != "All":
    filtered_df = filtered_df[
        filtered_df["kolektibilitas"].astype(str) == selected_kol
    ]

filtered_df = filtered_df.copy()


# =========================================================
# 10. PORTFOLIO METRICS
# =========================================================

n = len(filtered_df)

high_risk_count = int(
    (filtered_df["risk_level"] == "HIGH").sum()
)

medium_risk_count = int(
    (filtered_df["risk_level"] == "MEDIUM").sum()
)

low_risk_count = int(
    (filtered_df["risk_level"] == "LOW").sum()
)

high_risk_ratio = (
    high_risk_count / n * 100
    if n > 0 else 0
)

average_risk_score = (
    filtered_df["risk_score"].mean()
    if n > 0 else 0
)

average_dti = (
    filtered_df["debt_to_income"].mean()
    if n > 0 else 0
)

average_delinquency = (
    filtered_df["tunggakan_hari"].mean()
    if n > 0 else 0
)


# =========================================================
# 11. PROCESS RISK, EWS, EXPLANATION AND ACTION
# =========================================================

def run_row_module(function, row):
    """
    Menjalankan modul per debitur.
    Jika satu baris gagal diproses, dashboard tetap berjalan.
    """
    try:
        result = function(row)

        if isinstance(result, dict):
            return result

        return {"result": result}

    except Exception as error:
        return {
            "error": str(error)
        }


ranking_df = filtered_df.copy()

if not ranking_df.empty:

    # Recommended action
    ranking_df["recommended_action"] = ranking_df.apply(
        lambda row: safe_text(
            recommend_action(row),
            "Manual Review"
        ),
        axis=1
    )

    # Early warning
    ews_results = ranking_df.apply(
        lambda row: run_row_module(
            assess_early_warning,
            row
        ),
        axis=1
    )

    ranking_df["warning_score"] = ews_results.apply(
        lambda result: safe_float(
            result.get("warning_score", 0)
        )
    )

    ranking_df["ews_level"] = ews_results.apply(
        lambda result: normalize_level(
            result.get("ews_level", "LOW"),
            ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
        )
    )

    ranking_df["warning_count"] = ews_results.apply(
        lambda result: int(
            safe_float(result.get("warning_count", 0))
        )
    )

    ranking_df["warning_indicators"] = ews_results.apply(
        lambda result: format_explanation_value(
            result.get("warning_indicators", [])
        )
    )

    ranking_df["monitoring_priority"] = ews_results.apply(
        lambda result: safe_text(
            result.get("monitoring_priority", "-")
        )
    )

    # Risk explanation
    explanation_results = ranking_df.apply(
        lambda row: run_row_module(
            explain_risk,
            row
        ),
        axis=1
    )

    ranking_df["risk_drivers"] = explanation_results.apply(
        lambda result: format_explanation_value(
            result.get("risk_drivers", [])
        )
    )

    ranking_df["risk_explanation"] = explanation_results.apply(
        lambda result: safe_text(
            result.get("risk_explanation", "-")
        )
    )

    ranking_df["overall_explanation"] = explanation_results.apply(
        lambda result: safe_text(
            result.get(
                "overall_explanation",
                result.get("risk_explanation", "-")
            )
        )
    )

    # Action priority
    ranking_df["priority"] = ranking_df["risk_level"].map({
        "HIGH": "P1 - URGENT",
        "MEDIUM": "P2 - REVIEW",
        "LOW": "P3 - MONITOR"
    }).fillna("P3 - MONITOR")

    # EWS ranking
    ranking_df["ews_sort_order"] = (
        ranking_df["ews_level"]
        .map({
            "CRITICAL": 1,
            "HIGH": 2,
            "MEDIUM": 3,
            "LOW": 4
        })
        .fillna(5)
    )

    # Sort by EWS first, then warning score, risk score, delinquency
    ranking_df = ranking_df.sort_values(
        by=[
            "ews_sort_order",
            "warning_score",
            "risk_score",
            "tunggakan_hari"
        ],
        ascending=[
            True,
            False,
            False,
            False
        ]
    ).reset_index(drop=True)

    ranking_df = ranking_df.drop(
        columns=["ews_sort_order"]
    )

    ranking_df["priority_rank"] = range(
        1,
        len(ranking_df) + 1
    )

else:
    ranking_df["recommended_action"] = pd.Series(dtype="object")
    ranking_df["warning_score"] = pd.Series(dtype="float")
    ranking_df["ews_level"] = pd.Series(dtype="object")
    ranking_df["warning_count"] = pd.Series(dtype="int")
    ranking_df["warning_indicators"] = pd.Series(dtype="object")
    ranking_df["monitoring_priority"] = pd.Series(dtype="object")
    ranking_df["risk_drivers"] = pd.Series(dtype="object")
    ranking_df["risk_explanation"] = pd.Series(dtype="object")
    ranking_df["overall_explanation"] = pd.Series(dtype="object")
    ranking_df["priority"] = pd.Series(dtype="object")
    ranking_df["priority_rank"] = pd.Series(dtype="int")


# =========================================================
# 12. EWS SUMMARY
# =========================================================

ews_levels = [
    "CRITICAL",
    "HIGH",
    "MEDIUM",
    "LOW"
]

if not ranking_df.empty:
    ews_counts = (
        ranking_df["ews_level"]
        .value_counts()
        .reindex(ews_levels, fill_value=0)
    )
else:
    ews_counts = pd.Series(
        [0, 0, 0, 0],
        index=ews_levels
    )

critical_count = int(ews_counts["CRITICAL"])
high_count = int(ews_counts["HIGH"])
medium_count = int(ews_counts["MEDIUM"])
low_count = int(ews_counts["LOW"])

total_ews = len(ranking_df)

critical_high_count = (
    critical_count + high_count
)

critical_high_percentage = (
    critical_high_count / total_ews * 100
    if total_ews > 0 else 0
)

alert_df = (
    ranking_df[
        ranking_df["ews_level"].isin(
            ["CRITICAL", "HIGH", "MEDIUM"]
        )
    ].copy()
    if not ranking_df.empty
    else pd.DataFrame()
)


# =========================================================
# 13. PORTFOLIO INSIGHTS
# =========================================================

try:
    portfolio_insights = generate_portfolio_insights(
        filtered_df
    )

    if not isinstance(portfolio_insights, list):
        portfolio_insights = []

except Exception as error:
    portfolio_insights = []
    st.warning(
        f"Portfolio insight module tidak dapat dijalankan: {error}"
    )


def render_insights(insights, limit=4):

    if not insights:
        html_card("""
            <div class="insight-item insight-info">
                <span class="insight-tag">PORTFOLIO</span>
                <b>Portfolio Stable</b>
                <p>No significant portfolio insights detected.</p>
            </div>
        """)
        return

    for insight in insights[:limit]:

        if not isinstance(insight, dict):
            continue

        severity = safe_text(
            insight.get("severity", "INFO")
        ).upper()

        title = escape(
            safe_text(
                insight.get("title", "Portfolio Insight")
            )
        )

        message = escape(
            safe_text(
                insight.get("message", "")
            )
        )

        if severity == "CRITICAL":
            css_class = "insight-critical"
            tag = "CRITICAL"

        elif severity in ["WARNING", "HIGH"]:
            css_class = "insight-warning"
            tag = "ATTENTION"

        else:
            css_class = "insight-info"
            tag = "INSIGHT"

        html_card(f"""
            <div class="insight-item {css_class}">
                <span class="insight-tag">{tag}</span>
                <b>{title}</b>
                <p>{message}</p>
            </div>
        """)


# =========================================================
# 14. TOP DEBTOR TABLE
# =========================================================

def render_top_debtors(data, limit=5):

    if data is None or data.empty:
        show_empty("No debtor data available.")
        return

    display_df = data.head(limit).copy()

    # Gunakan tabel native Streamlit.
    # Tidak memakai HTML table agar tidak tampil sebagai teks/kode.
    table = pd.DataFrame({
        "Rank": range(1, len(display_df) + 1),
        "Debtor ID": display_df["debtor_id"].astype(str),
        "Risk Score": pd.to_numeric(
            display_df["risk_score"],
            errors="coerce"
        ).fillna(0),
        "Risk Level": display_df["risk_level"].astype(str),
        "Early Warning": display_df["ews_level"].astype(str)
    })

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True,
        height=min(250, 42 + (len(table) * 35)),
        column_config={
            "Rank": st.column_config.NumberColumn(
                "Rank",
                width="small"
            ),
            "Debtor ID": st.column_config.TextColumn(
                "Debtor ID",
                width="medium"
            ),
            "Risk Score": st.column_config.ProgressColumn(
                "Risk Score",
                min_value=0,
                max_value=100,
                format="%.1f"
            ),
            "Risk Level": st.column_config.TextColumn(
                "Risk Level",
                width="small"
            ),
            "Early Warning": st.column_config.TextColumn(
                "Early Warning",
                width="medium"
            )
        }
    )


# =========================================================
# 15. OVERVIEW
# =========================================================

if page == "Overview":

    # KPI ROW
    k1, k2, k3, k4 = st.columns(4, gap="small")

    with k1:
        kpi(
            "Filtered Debtors",
            f"{n:,}",
            "Borrowers in current selection",
            "◉",
            "blue"
        )

    with k2:
        kpi(
            "High Risk",
            f"{high_risk_count:,}",
            f"{high_risk_ratio:.1f}% of selection",
            "⚠",
            "red"
        )

    with k3:
        kpi(
            "Average Risk Score",
            f"{average_risk_score:.1f}",
            "Portfolio risk index",
            "⌁",
            "purple"
        )

    with k4:
        kpi(
            "Average DTI",
            f"{average_dti:.1%}",
            "Debt-to-income ratio",
            "↗",
            "teal"
        )

    # CHARTS
    chart_left, chart_right = st.columns(
        [1, 1.25],
        gap="small"
    )

    with chart_left:
        with st.container(border=True):

            card_title(
                "Portfolio Risk Distribution",
                "Borrower composition by risk level"
            )

            risk_dist = (
                filtered_df["risk_level"]
                .value_counts()
                .reindex(
                    ["LOW", "MEDIUM", "HIGH"],
                    fill_value=0
                )
            )

            fig = make_bar_chart(
                risk_dist.index,
                risk_dist.values,
                ["#20A779", "#E6B344", "#E65B68"],
                height=165
            )

            show_chart(fig)

    with chart_right:
        with st.container(border=True):

            card_title(
                "Early Warning Monitoring",
                "Active monitoring distribution"
            )

            ews_display = ews_counts.reindex(
                ["CRITICAL", "HIGH", "MEDIUM", "LOW"],
                fill_value=0
            )

            fig2 = make_horizontal_chart(
                ews_display.index,
                ews_display.values,
                ["#E65B68", "#F09543", "#E6B344", "#20A779"],
                height=165
            )

            show_chart(fig2)

    # BOTTOM SECTION
    col1, col2, col3 = st.columns(
        [0.82, 1.4, 1.12],
        gap="small"
    )

    # PRIORITY ALERTS
    with col1:

        card_title(
            "Priority Alerts",
            "Portfolio warning severity"
        )

        alert_items = [
            ("CRITICAL", critical_count, "✕", "critical"),
            ("HIGH", high_count, "⚠", "high"),
            ("MEDIUM", medium_count, "◉", "medium"),
            ("LOW", low_count, "✓", "low")
        ]

        alerts_html = ""

        for label, count, icon, css in alert_items:

            alerts_html += f"""
            <div class="alert-row {css}">
                <div class="alert-icon">{icon}</div>
                <span class="alert-name">{label}</span>
                <b>{count:,}</b>
            </div>
            """

        st.markdown(
            alerts_html,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="alert-foot">
                <b>{critical_high_count:,}</b> borrowers
                require priority attention
            </div>
            """,
            unsafe_allow_html=True
        )

    # TOP RISK DEBTORS
    with col2:

        card_title(
            "Top Risk Debtors",
            "Highest priority borrowers based on EWS and risk score"
        )

        render_top_debtors(
            ranking_df,
            limit=5
        )

    # KEY INSIGHTS
    with col3:

        card_title(
            "Key Insights",
            "AI portfolio intelligence"
        )

        render_insights(
            portfolio_insights,
            limit=4
        )


# =========================================================
# 16. RISK ANALYTICS
# =========================================================

elif page == "Risk Analytics":

    c1, c2, c3, c4 = st.columns(4, gap="small")

    with c1:
        kpi(
            "HIGH RISK",
            f"{high_risk_count:,}",
            "High risk borrowers",
            "⚠",
            "red"
        )

    with c2:
        kpi(
            "MEDIUM RISK",
            f"{medium_risk_count:,}",
            "Medium risk borrowers",
            "◉",
            "purple"
        )

    with c3:
        kpi(
            "LOW RISK",
            f"{low_risk_count:,}",
            "Low risk borrowers",
            "✓",
            "teal"
        )

    with c4:
        kpi(
            "AVG DTI",
            f"{average_dti:.1%}",
            "Debt-to-income ratio",
            "↗",
            "blue"
        )

    left, right = st.columns(2, gap="small")

    with left:
        with st.container(border=True):

            card_title(
                "Risk Level Distribution",
                "Number of borrowers by risk category"
            )

            risk_counts = (
                filtered_df["risk_level"]
                .value_counts()
                .reindex(
                    ["LOW", "MEDIUM", "HIGH"],
                    fill_value=0
                )
            )

            fig = make_bar_chart(
                risk_counts.index,
                risk_counts.values,
                ["#20A779", "#E6B344", "#E65B68"],
                height=210
            )

            show_chart(fig)

    with right:
        with st.container(border=True):

            card_title(
                "Credit Quality Distribution",
                "GOOD / WATCH / BAD borrower classification"
            )

            quality_counts = (
                filtered_df["credit_quality"]
                .value_counts()
                .reindex(
                    ["GOOD", "WATCH", "BAD"],
                    fill_value=0
                )
            )

            fig2 = make_bar_chart(
                quality_counts.index,
                quality_counts.values,
                ["#20A779", "#E6B344", "#E65B68"],
                height=210
            )

            show_chart(fig2)

    left2, right2 = st.columns(2, gap="small")

    with left2:
        with st.container(border=True):

            card_title(
                "DTI Category Analysis",
                "Debt-to-income segmentation"
            )

            dti_counts = (
                filtered_df["dti_category"]
                .value_counts()
                .reindex(
                    ["LOW", "MODERATE", "HIGH"],
                    fill_value=0
                )
            )

            fig3 = make_horizontal_chart(
                dti_counts.index,
                dti_counts.values,
                ["#246BFD", "#E6B344", "#E65B68"],
                height=205
            )

            show_chart(fig3)

    with right2:
        with st.container(border=True):

            card_title(
                "Risk Score Distribution",
                "Distribution of borrower risk scores"
            )

            fig4 = px.histogram(
                filtered_df,
                x="risk_score",
                nbins=20,
                color_discrete_sequence=["#246BFD"]
            )

            fig4.update_layout(
                **chart_layout(205),
                bargap=0.08,
                showlegend=False,
                xaxis=dict(
                    showgrid=False,
                    title="Risk Score"
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="#EDF1F6",
                    title="Number of Debtors"
                )
            )

            show_chart(fig4)

    st.markdown(
        "<div class='section-title'>Portfolio Risk Detail</div>",
        unsafe_allow_html=True
    )

    if not ranking_df.empty:

        risk_table = ranking_df.head(15)[[
            "debtor_id",
            "risk_level",
            "risk_score",
            "credit_quality",
            "debt_to_income",
            "tunggakan_hari"
        ]].copy()

        risk_table = risk_table.rename(
            columns={
                "debtor_id": "Debtor ID",
                "risk_level": "Risk Level",
                "risk_score": "Risk Score",
                "credit_quality": "Credit Quality",
                "debt_to_income": "Debt-to-Income Ratio",
                "tunggakan_hari": "Days Past Due"
            }
        )

        render_dataframe(
            risk_table,
            height=300,
            column_config={
                "Risk Score": st.column_config.NumberColumn(
                    "Risk Score",
                    format="%.1f"
                ),
                "Debt-to-Income Ratio": st.column_config.NumberColumn(
                    "Debt-to-Income Ratio",
                    format="percent"
                ),
                "Days Past Due": st.column_config.NumberColumn(
                    "Days Past Due",
                    format="%d"
                )
            }
        )

    else:
        show_empty("No risk records available.")


# =========================================================
# 17. EARLY WARNING
# =========================================================

elif page == "Early Warning":

    c1, c2, c3, c4 = st.columns(4, gap="small")

    with c1:
        kpi(
            "CRITICAL",
            f"{critical_count:,}",
            "Immediate attention",
            "✕",
            "red"
        )

    with c2:
        kpi(
            "HIGH",
            f"{high_count:,}",
            "Priority monitoring",
            "⚠",
            "red"
        )

    with c3:
        kpi(
            "MEDIUM",
            f"{medium_count:,}",
            "Periodic review",
            "◉",
            "purple"
        )

    with c4:
        kpi(
            "LOW",
            f"{low_count:,}",
            "Normal monitoring",
            "✓",
            "teal"
        )

    left, right = st.columns(
        [1, 1.35],
        gap="small"
    )

    with left:
        with st.container(border=True):

            card_title(
                "Warning Distribution",
                "Number of borrowers by monitoring severity"
            )

            fig = make_horizontal_chart(
                ews_counts.index,
                ews_counts.values,
                ["#E65B68", "#F09543", "#E6B344", "#20A779"],
                height=220
            )

            show_chart(fig)

    with right:
        with st.container(border=True):

            card_title(
                "Priority Monitoring Debtors",
                "Borrowers with active warning signals"
            )

            warning_df = ranking_df[
                ranking_df["ews_level"].isin(
                    ["CRITICAL", "HIGH", "MEDIUM"]
                )
            ].copy()

            render_top_debtors(
                warning_df,
                limit=8
            )

    st.markdown(
        "<div class='section-title'>Understanding Warning Indicators</div>",
        unsafe_allow_html=True
    )

    indicator_info = [
        (
            "Warning Score",
            "Numerical score representing the strength of detected warning signals."
        ),
        (
            "Warning Count",
            "Number of warning indicators detected for the borrower."
        ),
        (
            "Warning Indicators",
            "Specific conditions or factors that triggered an early warning."
        ),
        (
            "Monitoring Priority",
            "Suggested urgency level for follow-up and monitoring."
        )
    ]

    info_cols = st.columns(4, gap="small")

    for index, (label, description) in enumerate(indicator_info):

        with info_cols[index]:
            render_detail_box(
                label,
                "Indicator definition",
                description
            )

    st.markdown(
        "<div class='section-title'>Warning Indicator Detail</div>",
        unsafe_allow_html=True
    )

    if not alert_df.empty:

        warning_columns = [
            "debtor_id",
            "risk_level",
            "risk_score",
            "ews_level",
            "warning_score",
            "warning_count",
            "warning_indicators",
            "monitoring_priority"
        ]

        warning_table = alert_df[
            [
                column
                for column in warning_columns
                if column in alert_df.columns
            ]
        ].copy()

        warning_table = warning_table.rename(
            columns={
                "debtor_id": "Debtor ID",
                "risk_level": "Risk Level",
                "risk_score": "Risk Score",
                "ews_level": "EWS Severity",
                "warning_score": "Warning Score",
                "warning_count": "Warning Count",
                "warning_indicators": "Detected Warning Indicators",
                "monitoring_priority": "Monitoring Priority"
            }
        )

        render_dataframe(
            warning_table,
            height=320,
            column_config={
                "Risk Score": st.column_config.NumberColumn(
                    "Risk Score",
                    format="%.1f"
                ),
                "Warning Score": st.column_config.NumberColumn(
                    "Warning Score",
                    format="%.1f"
                ),
                "Warning Count": st.column_config.NumberColumn(
                    "Warning Count",
                    format="%d"
                ),
                "Detected Warning Indicators": st.column_config.TextColumn(
                    "Detected Warning Indicators",
                    width="large"
                ),
                "Monitoring Priority": st.column_config.TextColumn(
                    "Monitoring Priority"
                )
            }
        )

    else:
        show_empty("No active warning indicators.")


# =========================================================
# 18. DEBTOR INTELLIGENCE
# =========================================================

elif page == "Debtor Intelligence":

    st.markdown(
        "<div class='section-title'>Debtor Investigation</div>",
        unsafe_allow_html=True
    )

    debtor_ids = (
        eda_df["debtor_id"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_debtor = st.selectbox(
        "Search or Select Debtor ID",
        debtor_ids,
        key="debtor_search"
    )

    if selected_debtor:

        debtor_row = eda_df[
            eda_df["debtor_id"].astype(str) == str(selected_debtor)
        ]

        if not debtor_row.empty:

            row = debtor_row.iloc[0]

            # DEBTOR KPI
            c1, c2, c3, c4 = st.columns(4, gap="small")

            with c1:
                kpi(
                    "Risk Score",
                    f"{safe_float(row.get('risk_score')):.1f}",
                    "Borrower risk index",
                    "⌁",
                    "purple"
                )

            with c2:
                kpi(
                    "Risk Level",
                    safe_text(row.get("risk_level")),
                    "Credit risk category",
                    "⚠",
                    "red"
                )

            with c3:
                kpi(
                    "Credit Quality",
                    safe_text(row.get("credit_quality")),
                    "Quality assessment",
                    "◉",
                    "blue"
                )

            with c4:
                kpi(
                    "DTI",
                    f"{safe_float(row.get('debt_to_income')):.1%}",
                    "Debt-to-income ratio",
                    "↗",
                    "teal"
                )

            left, right = st.columns(
                [1, 1.25],
                gap="small"
            )

            # BORROWER PROFILE
            with left:
                with st.container(border=True):

                    card_title(
                        "Borrower Profile",
                        "Selected debtor information"
                    )

                    profile_items = [
                        ("Debtor ID", row.get("debtor_id", "-")),
                        ("Risk Level", row.get("risk_level", "-")),
                        ("Risk Score", row.get("risk_score", "-")),
                        ("Credit Quality", row.get("credit_quality", "-")),
                        ("DTI Category", row.get("dti_category", "-")),
                        ("Kolektibilitas", row.get("kolektibilitas", "-")),
                        ("Days Past Due", row.get("tunggakan_hari", "-"))
                    ]

                    for label, value in profile_items:

                        a, b = st.columns([1, 1.2])

                        with a:
                            st.markdown(
                                f"""
                                <div class='detail-label'>
                                    {escape(str(label))}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        with b:
                            st.markdown(
                                f"""
                                <div class='detail-value'>
                                    {escape(safe_text(value))}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        st.divider()

            # INVESTIGATION
            with right:
                with st.container(border=True):

                    card_title(
                        "Investigation Result",
                        "Structured borrower investigation"
                    )

                    investigation = run_row_module(
                        investigate_debtor,
                        row
                    )

                    if investigation.get("error"):

                        st.warning(
                            "Investigation module: "
                            + investigation["error"]
                        )

                    else:

                        investigation_items = list(
                            investigation.items()
                        )

                        if investigation_items:

                            for start in range(
                                0,
                                len(investigation_items),
                                2
                            ):

                                pair = investigation_items[
                                    start:start + 2
                                ]

                                cols = st.columns(
                                    len(pair),
                                    gap="small"
                                )

                                for col, (key, value) in zip(
                                    cols,
                                    pair
                                ):

                                    with col:

                                        label = (
                                            str(key)
                                            .replace("_", " ")
                                            .title()
                                        )

                                        render_detail_box(
                                            label,
                                            format_explanation_value(value)
                                        )

                        else:
                            show_empty(
                                "No investigation details returned."
                            )

            # RISK EXPLANATION
            st.markdown(
                "<div class='section-title'>Risk Explanation</div>",
                unsafe_allow_html=True
            )

            explanation = run_row_module(
                explain_risk,
                row
            )

            if explanation.get("error"):

                st.warning(
                    "Risk explanation unavailable: "
                    + explanation["error"]
                )

            else:

                drivers = explanation.get(
                    "risk_drivers",
                    []
                )

                overall = explanation.get(
                    "overall_explanation",
                    explanation.get("risk_explanation", "-")
                )

                risk_reason = explanation.get(
                    "risk_explanation",
                    "-"
                )

                exp_left, exp_right = st.columns(
                    2,
                    gap="small"
                )

                with exp_left:
                    with st.container(border=True):

                        card_title(
                            "Risk Drivers",
                            "Factors contributing to borrower risk"
                        )

                        if isinstance(drivers, (list, tuple)):

                            if drivers:

                                chips = ""

                                for driver in drivers:
                                    chips += (
                                        "<span class='driver-chip'>"
                                        f"{escape(str(driver))}"
                                        "</span>"
                                    )

                                st.markdown(
                                    chips,
                                    unsafe_allow_html=True
                                )

                            else:
                                show_empty(
                                    "No significant risk drivers."
                                )

                        else:
                            st.write(drivers)

                with exp_right:
                    with st.container(border=True):

                        card_title(
                            "Overall Assessment",
                            "Summary of borrower risk condition"
                        )

                        st.markdown(
                            f"""
                            <div class="explanation-box">
                                <p>{escape(str(overall))}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                with st.container(border=True):

                    card_title(
                        "Risk Explanation Detail",
                        "Additional explanation from risk assessment"
                    )

                    st.write(risk_reason)


# =========================================================
# 19. ACTION CENTER
# =========================================================

elif page == "Action Center":

    p1_count = (
        int(
            (ranking_df["priority"] == "P1 - URGENT").sum()
        )
        if not ranking_df.empty else 0
    )

    p2_count = (
        int(
            (ranking_df["priority"] == "P2 - REVIEW").sum()
        )
        if not ranking_df.empty else 0
    )

    p3_count = (
        int(
            (ranking_df["priority"] == "P3 - MONITOR").sum()
        )
        if not ranking_df.empty else 0
    )

    # PRIORITY KPIs
    c1, c2, c3, c4 = st.columns(4, gap="small")

    with c1:
        kpi(
            "URGENT ACTION",
            f"{p1_count:,}",
            "P1 borrowers",
            "⚠",
            "red"
        )

    with c2:
        kpi(
            "REVIEW",
            f"{p2_count:,}",
            "P2 borrowers",
            "◉",
            "purple"
        )

    with c3:
        kpi(
            "MONITOR",
            f"{p3_count:,}",
            "P3 borrowers",
            "✓",
            "teal"
        )

    with c4:
        kpi(
            "TOTAL CASES",
            f"{len(ranking_df):,}",
            "Filtered portfolio",
            "▣",
            "blue"
        )

    # ACTION SUMMARY
    left, right = st.columns(
        [0.85, 1.4],
        gap="small"
    )

    with left:
        with st.container(border=True):

            card_title(
                "Action Priority",
                "Borrower follow-up prioritization"
            )

            action_counts = pd.Series({
                "URGENT": p1_count,
                "REVIEW": p2_count,
                "MONITOR": p3_count
            })

            fig = make_horizontal_chart(
                action_counts.index,
                action_counts.values,
                ["#E65B68", "#E6B344", "#20A779"],
                height=220
            )

            show_chart(fig)

    with right:
        with st.container(border=True):

            card_title(
                "Recommended Actions",
                "Priority borrower follow-up"
            )

            if not ranking_df.empty:

                action_display = ranking_df.head(10).copy()

                display_cols = [
                    column
                    for column in [
                        "priority_rank",
                        "debtor_id",
                        "priority",
                        "risk_level",
                        "risk_score",
                        "ews_level",
                        "monitoring_priority",
                        "recommended_action"
                    ]
                    if column in action_display.columns
                ]

                action_display = action_display[
                    display_cols
                ].rename(
                    columns={
                        "priority_rank": "Rank",
                        "debtor_id": "Debtor ID",
                        "priority": "Action Priority",
                        "risk_level": "Risk Level",
                        "risk_score": "Risk Score",
                        "ews_level": "EWS Severity",
                        "monitoring_priority": "Monitoring Priority",
                        "recommended_action": "Recommended Action"
                    }
                )

                render_dataframe(
                    action_display,
                    height=350,
                    column_config={
                        "Rank": st.column_config.NumberColumn(
                            "Rank"
                        ),
                        "Risk Score": st.column_config.NumberColumn(
                            "Risk Score",
                            format="%.1f"
                        ),
                        "Recommended Action": st.column_config.TextColumn(
                            "Recommended Action",
                            width="large"
                        )
                    }
                )

            else:
                show_empty("No action cases available.")

    # PRIORITY DETAILS
    st.markdown(
        "<div class='section-title'>Critical & High Priority Cases</div>",
        unsafe_allow_html=True
    )

    if not ranking_df.empty:

        urgent_df = ranking_df[
            ranking_df["ews_level"].isin(
                ["CRITICAL", "HIGH"]
            )
        ].copy()

        if not urgent_df.empty:

            urgent_columns = [
                column
                for column in [
                    "debtor_id",
                    "risk_level",
                    "risk_score",
                    "ews_level",
                    "warning_score",
                    "warning_count",
                    "warning_indicators",
                    "recommended_action",
                    "monitoring_priority"
                ]
                if column in urgent_df.columns
            ]

            urgent_table = urgent_df[
                urgent_columns
            ].rename(
                columns={
                    "debtor_id": "Debtor ID",
                    "risk_level": "Risk Level",
                    "risk_score": "Risk Score",
                    "ews_level": "EWS Severity",
                    "warning_score": "Warning Score",
                    "warning_count": "Warning Count",
                    "warning_indicators": "Detected Warning Indicators",
                    "recommended_action": "Recommended Action",
                    "monitoring_priority": "Monitoring Priority"
                }
            )

            render_dataframe(
                urgent_table,
                height=320,
                column_config={
                    "Risk Score": st.column_config.NumberColumn(
                        "Risk Score",
                        format="%.1f"
                    ),
                    "Warning Score": st.column_config.NumberColumn(
                        "Warning Score",
                        format="%.1f"
                    ),
                    "Warning Count": st.column_config.NumberColumn(
                        "Warning Count",
                        format="%d"
                    ),
                    "Detected Warning Indicators": st.column_config.TextColumn(
                        "Detected Warning Indicators",
                        width="large"
                    ),
                    "Recommended Action": st.column_config.TextColumn(
                        "Recommended Action",
                        width="large"
                    )
                }
            )

        else:
            show_empty(
                "No critical or high priority cases."
            )

    else:
        show_empty("No portfolio records.")
