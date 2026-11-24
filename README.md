# banking-ai-copilot
An LLM-powered banking assistant for credit policy retrieval, risk analytics, and AI evaluation.
# 🏦 Banking AI Copilot
### Credit Risk Analytics, Early Warning System & Decision Support

A Python-based banking analytics application designed to support credit risk monitoring, debtor prioritization, portfolio analysis, early warning detection, and risk-based action recommendations.

Banking AI Copilot transforms debtor-level financial indicators into structured risk insights through a rule-based credit risk engine, explainable risk assessment, and an interactive Streamlit dashboard.

## Overview

This project simulates a credit risk monitoring and decision-support system that helps identify potential credit deterioration, analyze debtor risk characteristics, and prioritize monitoring activities.

The application integrates data processing, risk scoring, portfolio intelligence, early warning signals, and debtor investigation into a single analytical dashboard.

## Key Features

- **Credit Risk Scoring** — Evaluates debtor risk based on predefined risk indicators and scoring rules.
- **Feature Engineering** — Generates DTI categories, delinquency classifications, and credit quality indicators.
- **Portfolio Intelligence** — Automatically identifies portfolio risk concentrations and potential warning patterns.
- **Early Warning System (EWS)** — Detects risk signals and assigns warning levels and monitoring priorities.
- **Risk Explainability** — Identifies risk drivers and generates structured explanations for debtor risk assessments.
- **Action Recommendation** — Provides risk-based recommended actions and monitoring suggestions.
- **Debtor Investigation Profile** — Summarizes financial condition, payment condition, credit assessment, risk signals, and investigation recommendations.
- **Portfolio Risk Ranking** — Prioritizes debtors based on warning scores, risk scores, and delinquency.
- **Interactive Dashboard** — Visualizes portfolio risk distribution, credit quality, DTI, delinquency, alerts, and debtor-level analysis.

## System Architecture

```text
Debtor Dataset
      │
      ▼
Data Processing & Feature Engineering
      │
      ▼
Credit Risk Engine
      │
      ├── Risk Scoring
      ├── Risk Classification
      ├── Risk Explainer
      └── Action Recommendation
      │
      ▼
Early Warning System
      │
      ├── Warning Score
      ├── Warning Indicators
      ├── EWS Classification
      └── Monitoring Priority
      │
      ▼
Debtor Investigation & Prioritization
      │
      ▼
Streamlit Dashboard
      │
      ├── Portfolio Intelligence
      ├── Executive KPIs
      ├── Risk Analysis
      ├── Early Warning Monitoring
      ├── Debtor Ranking
      └── Investigation Profile
```

## Dashboard Modules

### Portfolio Intelligence
Automated portfolio diagnostics and risk insights based on the selected portfolio.

### Executive Portfolio Overview
Provides key portfolio indicators, including debtor count, high-risk concentration, average risk score, and average DTI.

### Risk Analytics
Analyzes risk distribution, credit quality, debt-to-income, risk segmentation, and delinquency characteristics.

### Early Warning System
Identifies debtors with potential risk signals and categorizes them into CRITICAL, HIGH, MEDIUM, and LOW warning levels.

### Risk Monitoring Action Center
Displays debtors requiring additional monitoring, alert concentration, warning indicators, and recommended follow-up actions.

### Debtor Explainability Explorer
Provides individual debtor analysis, including risk drivers, risk explanations, financial profile, EWS profile, monitoring priority, and recommendations.

## Technology Stack

- Python
- Pandas
- Streamlit
- Data Analytics
- Rule-Based Risk Scoring
- Feature Engineering
- Explainable Analytics
- Data Visualization

## Project Structure

```text
banking-ai-copilot/
│
├── data/
│   └── sample/
│       └── debtors.csv
│
├── src/
│   ├── risk_engine.py
│   ├── action_recommendation.py
│   ├── risk_explainer.py
│   ├── insight_generator.py
│   ├── early_warning.py
│   └── debtor_investigation.py
│
├── feature_engineering.py
├── main.py
├── dashboard.py
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/alfreddownmountsimaremare/banking-ai-copilot.git
cd banking-ai-copilot
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Run the analytical pipeline:

```bash
python main.py
```

Launch the interactive dashboard:

```bash
streamlit run dashboard.py
```

## Analytical Indicators

The application evaluates several simulated credit risk indicators:

| Indicator | Purpose |
|---|---|
| Debt-to-Income Ratio | Evaluates debt burden relative to income |
| Delinquency Days | Measures payment delays |
| Delinquency Category | Classifies payment conditions |
| Credit Quality | Categorizes debtor credit condition |
| Risk Score | Quantifies rule-based risk assessment |
| Risk Level | Categorizes overall risk |
| Warning Score | Measures accumulated early warning signals |
| EWS Level | Determines warning severity |
| Monitoring Priority | Prioritizes follow-up activities |

## Disclaimer

This project is developed for educational, analytical, and portfolio demonstration purposes using synthetic debtor data.

Risk scoring, warning thresholds, classifications, and recommendations are based on predefined simulation rules. They do not represent official banking policies, validated credit models, actual customer data, or production banking decision systems.

The application is intended to demonstrate analytical workflow development, risk monitoring concepts, explainable decision support, and dashboard engineering.

## Author

**Alfred Downmount Simaremare**

Mathematics Graduate | Risk Analytics | Data Analytics | Banking Technology

GitHub: [alfreddownmountsimaremare](https://github.com/alfreddownmountsimaremare)