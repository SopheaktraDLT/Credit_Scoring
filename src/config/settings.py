import os

NUMERIC_FEATURES = {
    "age",
    "dependents",
    "monthly_income",
    "monthly_outflow",
    "net_cash_flow",
    "income_source_diversity",
    "expense_ratio",
    "dti_ratio",
    "lti_ratio",
    "loan_amount",
    "loan_tenure",
    "existing_loan_count",
    "total_debt_amount",
    "monthly_debt_payment",
    "surplus_income",
    "affordability_ratio",
    "loan_cycle_count",
    "on_time_payment_ratio",
    "max_dpd",
    "early_repayment_count",
    "saving_indicator",
    "is_urban",
    "guarantee_support",
}

# Database connection settings for the credit_system schema.
# Configure these values with environment variables for local development.
DB_CONFIG = {
    "host": os.getenv("CREDIT_DB_HOST", "localhost"),
    "user": os.getenv("CREDIT_DB_USER", "root"),
    "password": os.getenv("CREDIT_DB_PASSWORD", ""),
    "database": os.getenv("CREDIT_DB_NAME", "credit_system"),
}

GENDER_OPTIONS = ["Male", "Female"]

RELATIONSHIP_OPTIONS = [
    "New Applicant",
    "Existing Customer",
    "Referral",
    "Other"
]

INDUSTRY_OPTIONS = ["Service", "Business", "Delivery", "Building", "Other"]
POSITION_OPTIONS = [
    "Co-Founder",
    "Deputy Head of Department",
    "Director",
    "Founder",
    "Head of Department",
    "Manager",
    "Officer",
    "Senior Manager",
    "Skilled Worker",
    "Staff",
    "Worker",
    "Other",
]
LOAN_PURPOSE_OPTIONS = [
    "Living Expense",
    "Medical",
    "Wedding",
    "Bill Payment Services",
    "Repair of the House",
    "Travel",
    "Shopping",
    "Vehicles",
    "Other",
]
EMPLOYMENT_TYPE_OPTIONS = ["Government Officer", "Employee", "Business Owner", "Other"]
EMPLOYMENT_TENURE_OPTIONS = [
    "< 3 months",
    "3 - 6 months",
    "6 - 12 months",
    "1 - 3 years",
    "> 3 years",
]
WORK_EXPERIENCE_OPTIONS = [
    "< 1 year",
    "1 - 3 years",
    "3 - 6 years",
    "6 - 9 years",
    "> 9 years",
]
PROVINCES = ["Phnom Penh", "Kandal", "Siem Reap", "Other"]
DISTRICTS = ["D1", "D2", "D3", "Other"]
COMMUNES = ["C1", "C2", "C3", "Other"]
VILLAGES = ["V1", "V2", "V3", "Other"]
LOAN_TENURE_OPTIONS = [15, 30, 60, 90, 120, 180]
APPLICATION_FREQ_OPTIONS = ["1/month", "2/month", "3+/month"]
REBORROW_FREQ_OPTIONS = [">30 days", "7-30 days", "<7 days"]
YES_NO_OPTIONS = ["Yes", "No"]
PHONE_AGE_OPTIONS = [">5 Years", ">4 Years", ">3 Years", ">1.5 Years", "<1.5 Years"]
ID_VERIFICATION_OPTIONS = ["Verified", "Unverified"]
EMPLOYMENT_VERIFICATION_OPTIONS = ["Verified", "Not Verified"]
SOCIAL_LINK_OPTIONS = ["3+ Accounts", "2 Accounts", "1 Account", "None"]
ASSET_OPTIONS = ["Car", "Motobike", "Computer", "Phone", "None", "Other"]
RESIDENCE_OPTIONS = ["Self-Owned", "Parent's", "Rented", "Sibling", "Company"]
LIVING_DURATION_OPTIONS = ["< 3 months", "< 6 months", "< 1 year", "1-2 years", "2-3 years", "> 3 years"]

# Additional configuration options for NEW USER
INCOME_SOURCE_OPTIONS = ["1 source", "2 sources", "3+ sources"]
MARITAL_OPTIONS = ["single", "married", "divorced"]
EDUCATION_OPTIONS = ["PhD", "Master", "Bachelor", "High school", "Other"]
GUARANTEE_OPTIONS = ["Yes", "No"]
PHONE_AGE_OPTIONS = ["> 5 Years", "> 4 Years", "> 3 Years", "> 1.5 Years", "< 1.5 Years"]
SOCIAL_LINKS_OPTIONS = ["0", "1 Account", "2 Accounts", "3+ Accounts"]
ASSET_OPTIONS = ["Car", "Motobike", "Computer", "Phone"]
APPLICATION_FREQUENCY_OPTIONS = ["1/month", "2/month", "3+/month"]
BUSINESS_DURATION_OPTIONS = ["< 3 Months", "< 6 Month", "< 12 Months", "< 24 Months", "< 30 Months", "> 30 Months"]

# Additional options for OLD USER
ON_TIME_PAYMENT_OPTIONS = ["≥ 95%", "85 - 94%", "70 - 84%", "50 - 69%", "< 50%"]
MAX_DPD_OPTIONS = ["0 days", "1 - 15 days", "> 15 days"]
EARLY_REPAYMENT_OPTIONS = ["> 50%", "> 40%", "> 30%", "> 20%", "> 10%", "< 10%"]
PARTIAL_PAYMENT_OPTIONS = ["> 50%", "> 40%", "> 30%", "> 20%", "> 10%", "< 10%"]
REBORROW_FREQUENCY_OPTIONS = ["> 30 days", "7-30 days", "< 7 days"]
LOAN_AMOUNT_OLD_USER_OPTIONS = ["$50", "$100", "$150", "$200", "$250", "$300", "$350", "$400", "$500"]
