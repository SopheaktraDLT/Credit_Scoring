# Credit Scoring

AI-Based Credit Scoring System is a Streamlit application for loan decision support. It evaluates new and existing applicants, predicts default risk with trained machine learning models, calculates a transparent rule-based score breakdown, and stores assessment results in a MySQL database.

## Features

- New applicant and existing customer assessment workflows
- National ID lookup to route applicants into new-user or old-user forms
- Model selection for Random Forest, Logistic Regression, Support Vector Machine, and Neural Network predictions
- Adjustable decision threshold for default probability classification
- Identity verification checks before final loan recommendation
- Detailed credit score breakdown by scoring component and feature
- Assessment result saving to MySQL tables
- Assessment History dashboard with search, KPI metrics, and pagination

## Project Structure

```text
credit_scoring/
│
├── app.py
│   └── Main Streamlit application entry point.
│
├── model/
│   ├── new_user/
│   │   └── Trained machine learning models for new customers.
│   └── old_user/
│       └── Trained machine learning models for existing customers.
│
├── preprocessor/
│   ├── new_user/
│   │   └── Saved preprocessing pipeline for new customer assessment.
│   └── old_user/
│       └── Saved preprocessing pipeline for existing customer assessment.
│
├── src/
│   │
│   ├── config/
│   │   └── Application settings, constants, and database configuration.
│   │
│   ├── prediction/
│   │   ├── model_loader.py
│   │   │   └── Loads trained models and preprocessors.
│   │   └── predictor.py
│   │       └── Handles prediction generation and model inference.
│   │
│   ├── scoring/
│   │   ├── base.py
│   │   ├── rules.py
│   │   ├── breakdown.py
│   │   └── utils.py
│   │   └── Credit scoring logic, business rules, and score calculation.
│   │
│   ├── ui/
│   │   ├── components.py
│   │   ├── helpers.py
│   │   └── pages/
│   │       ├── history.py
│   │       ├── new_user_form.py
│   │       └── old_user_form.py
│   │   └── User interface components and application pages.
│   └──  
│
├── database.sql
│   └── db_manager.py
│        └──Database schema, views, and stored procedures.
│   └── database_schema.sql
│        └── Database connection and assessment record management.
│
├── requirements.txt
│   └── Python dependencies required to run the application.
│
├── README.md
│   └── Project documentation.
│
└── .gitignore
    └── Files and folders excluded from Git tracking.
```

## Workflow

1. The user starts the Streamlit app and chooses either `Credit Assessment` or `Assessment History`.
2. In `Credit Assessment`, the sidebar lets the user select a prediction model and decision threshold.
3. The user enters a National ID and clicks `Check`.
4. If the NID exists in the database, the app loads the existing customer workflow and includes repayment behavior fields.
5. If the NID is not found, the app uses the new applicant workflow.
6. The user completes personal, employment, residence, financial, loan, and verification fields.
7. Clicking `Prediction` builds the model input record, applies the correct preprocessor, and predicts default probability.
8. The system applies identity verification guard checks.
9. The app displays risk level, default probability, final credit score, detailed scoring breakdown, and approve/review/reject recommendation.
10. The assessment is saved to the `credit_system` MySQL database.
11. `Assessment History` reads saved assessments, shows summary metrics, supports searching by NID or name, and paginates results.

## Setup

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create the MySQL database

Run the schema file in MySQL:

```bash
mysql -u root -p < src/database/database_schema.sql
```

### 4. Configure database environment variables

PowerShell example:

```powershell
$env:CREDIT_DB_HOST="localhost"
$env:CREDIT_DB_USER="root"
$env:CREDIT_DB_PASSWORD="your_mysql_password"
$env:CREDIT_DB_NAME="credit_system"
```

The app reads these values from `src/config/settings.py`.

### 5. Add model assets locally

The trained model and preprocessor files are not committed because they are large binary files. Add them locally before running the app:

```text
model/new_user/NEW_RF.pkl
model/new_user/NEW_LR.pkl
model/new_user/NEW_SVM.pkl
model/new_user/NEW_MLP.pkl
model/old_user/OLD_RF.pkl
model/old_user/OLD_LR.pkl
model/old_user/OLD_SVM.pkl
model/old_user/OLD_MLP.pkl
preprocessor/new_user/new_preprocessor.pkl
preprocessor/old_user/old_preprocessor.pkl
```

## Run

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## Main Modules

- `app.py` controls the Streamlit navigation, user routing, prediction flow, and database saving.
- `src/ui/pages/new_user_form.py` renders the new applicant input workflow.
- `src/ui/pages/old_user_form.py` renders the existing customer input workflow.
- `src/ui/pages/history.py` renders the assessment history dashboard.
- `src/prediction/model_loader.py` loads preprocessors and ML models.
- `src/prediction/predictor.py` prepares model input and returns default risk predictions.
- `src/scoring/rules.py` defines individual rule-based scoring functions.
- `src/scoring/breakdown.py` builds the detailed scoring breakdown and final score.
- `src/database/db_manager.py` handles MySQL reads and assessment persistence.

## Notes

- Do not commit local database passwords. Use the `CREDIT_DB_*` environment variables instead.
- Generated Python cache files are ignored by `.gitignore`.
- Trained `.pkl` assets are ignored by Git and should be managed locally or through external storage.
