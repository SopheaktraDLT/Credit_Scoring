import streamlit as st
import numpy as np
from src.config.settings import *


def render_new_user_form(
    first_name,
    last_name,
    gender,
    relationship_with_platform,
    POSITION_OPTIONS_BY_EMPLOYMENT,
    n_id,
):
    """
    Renders the data input tab grouping designed for New User Applicant risk assessment.
    Captures profile data across 6 semantic areas, calculates basic financial ratios on-the-fly,
    and returns a local scope context dictionary containing all parameters needed for prediction models.
    """
    st.markdown(
        '<div class="panel-title">New User Assessment</div>', unsafe_allow_html=True
    )

    # Construct the primary structure interface separating the evaluation parameters
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["Applicant", "Capacity", "Debt", "Stability", "Identity", "Loan Profile"]
    )

    # --- TAB 1: APPLICANT PROFILE SUMMARY ---
    with tab1:
        st.subheader("Applicant profile")
        st.markdown(
            '<div class="section-callout">Personal details and relationship summary for underwriting review.</div>',
            unsafe_allow_html=True,
        )

        profile_col1, profile_col2 = st.columns(2)

        with profile_col1:
            col1, col2 = st.columns(2)
            with col1:
                age = st.number_input("Age", 18, 100, 30)
                marital_status = st.selectbox(
                    "Marital Status", MARITAL_OPTIONS, index=1
                )
                dependents = st.number_input("Dependents", 1, 10, 1)
            with col2:
                residence_type = st.selectbox(
                    "Residence Type", RESIDENCE_OPTIONS, index=0
                )
                living_duration = st.selectbox(
                    "Living Duration", LIVING_DURATION_OPTIONS, index=4
                )

        # Right column acts as a static visual confirmation block echoing sidebar inputs
        with profile_col2:
            st.markdown("**Applicant summary**")
            st.markdown(
                f"""
            <div class="card-container">
                <div class="profile-table">
                    <div class="profile-row"><strong>First Name</strong><span>:  {first_name}</span></div>
                    <div class="profile-row"><strong>Last Name</strong><span>:  {last_name}</span></div>
                    <div class="profile-row"><strong>Gender</strong><span>:  {gender}</span></div>
                    <div class="profile-row"><strong>Relationship</strong><span>:  {relationship_with_platform}</span></div>
                    <div class="profile-row"><strong>Location</strong><span>:  {residence_type}</span></div>
                    <div class="profile-row"><strong>Dependents</strong><span>:  {dependents}</span></div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    # --- TAB 2: FINANCIAL CAPACITY METRICS ---
    with tab2:
        st.subheader("Financial capacity")
        st.markdown("_Defines income, expense coverage and repayment ability._")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Income details**")
            monthly_income = st.number_input("Monthly Income ($)", 0.0, 500000.0, 600.0)
            income_source_diversity = st.selectbox(
                "Income Sources", INCOME_SOURCE_OPTIONS, index=0
            )

        with col2:
            st.markdown("**Expense profile**")
            monthly_outflow = st.number_input(
                "Monthly Outflow ($)", 0.0, 500000.0, 350.0
            )

        with col3:
            st.markdown("**Credit support**")
            guarantee_support = st.selectbox("Guarantee Support", GUARANTEE_OPTIONS)

        # Core mathematical ratio definitions evaluating survival/disposable revenue streams
        expense_ratio_decimal = (
            (monthly_outflow / monthly_income) if monthly_income > 0 else 0.0
        )
        expense_ratio_percent = expense_ratio_decimal * 100
        net_cash_flow_val = monthly_income - monthly_outflow

        metric_col1, metric_col2, metric_col3 = st.columns(3)
        with metric_col1:
            st.metric("Monthly Income", f"${monthly_income:,.0f}")
        with metric_col2:
            st.metric("Net Cash Flow", f"${net_cash_flow_val:,.0f}")
        with metric_col3:
            st.metric("Expense Ratio", f"{expense_ratio_percent:.1f}%")

    # --- TAB 3: DEBT RISK PROFILE ---
    with tab3:
        st.subheader("Debt profile")
        st.markdown("_Measures current debt, new loan burden, and affordability._")

        debt_col1, debt_col2 = st.columns(2)
        with debt_col1:
            st.markdown("**New loan request**")
            loan_amount_str = st.selectbox(
                "Loan Amount ($)", LOAN_AMOUNT_OLD_USER_OPTIONS
            )
            # Parse drop-down string option back to standard decimal calculation state
            loan_amount = float(loan_amount_str.replace("$", ""))
            loan_tenure = st.selectbox("Loan Tenure (days)", LOAN_TENURE_OPTIONS)

        with debt_col2:
            st.markdown("**Existing obligations**")
            total_debt_amount = st.number_input("Total Debt ($)", 0.0, 500000.0, 0.0)
            monthly_debt_payment = st.number_input(
                "Monthly Debt Payment ($)", 0.0, 500000.0, 0.0
            )
            existing_loan_count = st.number_input("Active Loans", 0, 10, 0)

        # Leverage index mathematical computations
        dti_ratio = (total_debt_amount / monthly_income) if monthly_income > 0 else 0.0
        lti_ratio = (loan_amount / monthly_income) if monthly_income > 0 else 0.0
        affordability_ratio = (
            ((loan_amount / loan_tenure) / monthly_income)
            if monthly_income > 0 and loan_tenure > 0
            else 0.0
        )
        tenure_months = max(loan_tenure / 30, 1)
        estimated_monthly_payment = loan_amount / tenure_months
        surplus_income = (
            monthly_income
            - monthly_outflow
            - monthly_debt_payment
            - estimated_monthly_payment
        )

        st.markdown("**Affordability summary**")

        risk_cols = st.columns(5)
        risk_cols[0].metric("DTI ratio", f"{dti_ratio:.1%}")
        risk_cols[1].metric("LTI ratio", f"{lti_ratio:.1%}")
        risk_cols[2].metric("Affordability", f"{affordability_ratio:.1%}")
        risk_cols[3].metric(
            "Monthly Loan Payment", f"${estimated_monthly_payment:,.0f}"
        )
        risk_cols[4].metric("Surplus income", f"${surplus_income:,.0f}")

    # --- TAB 4: STABILITY & OCCUPATION ANALYSIS ---
    with tab4:
        st.subheader("Stability & employment")
        st.markdown("_Assesses job stability, industry risk and experience._")

        stability_col1, stability_col2 = st.columns(2)
        with stability_col1:
            industry_type = st.selectbox("Industry Type", INDUSTRY_OPTIONS, index=0)
            employment_type = st.selectbox(
                "Employment Type", EMPLOYMENT_TYPE_OPTIONS, index=1
            )
            # Filter valid professional title definitions dynamically based on general career stream
            position_options = POSITION_OPTIONS_BY_EMPLOYMENT.get(
                employment_type, POSITION_OPTIONS
            )
            position = st.selectbox("Position", position_options)
            work_experience = st.selectbox("Work Experience", WORK_EXPERIENCE_OPTIONS)

        with stability_col2:
            education_level = st.selectbox(
                "Education Level", EDUCATION_OPTIONS, index=2
            )
            is_urban = st.selectbox("Urban Location", ["Yes", "No"])
            business_creation_time = None
            employment_tenure = None

            # Conditionally request tenure tracking variants based on operational profile class
            if employment_type == "Business Owner":
                business_creation_time = st.selectbox(
                    "Business Creation Time", BUSINESS_DURATION_OPTIONS
                )
            else:
                employment_tenure = st.selectbox(
                    "Employment Tenure", EMPLOYMENT_TENURE_OPTIONS
                )

    # --- TAB 5: KYC IDENTITY VERIFICATION CHECK ---
    with tab5:
        st.subheader("Identity verification")
        st.markdown(
            "_Capture key verification signals before proceeding with credit scoring._"
        )

        identity_col1, identity_col2 = st.columns(2)
        with identity_col1:
            face_match = st.selectbox("Face Match with ID", ["matched", "not matched"])
            phone_number_age = st.selectbox(
                "Phone Number Age", PHONE_AGE_OPTIONS, index=2
            )
        with identity_col2:
            employment_verified = st.selectbox("Employment Verified", ["yes", "no"])
            social_linked = st.selectbox("Social Linked Accounts", SOCIAL_LINKS_OPTIONS)

            # Use basic text validation check to determine NID profile token integrity
            nid_check = "valid" if n_id and len(n_id.strip()) > 0 else "invalid"
            if nid_check == "valid":
                st.success("✓ National ID Verified")
            else:
                st.warning("⚠ National ID Missing")

    # --- TAB 6: INTENT AND RESILIENCE CHARACTERISTICS ---
    with tab6:
        st.subheader("Loan purpose & resilience")
        st.markdown("_Review the loan purpose, borrowing behavior and savings buffer._")

        purpose_col1, purpose_col2 = st.columns(2)
        with purpose_col1:
            purpose_category = st.selectbox(
                "Purpose Category", ["expand_business", "payment", "other"]
            )
            business_type = "startup"
            business_duration = None
            payment_type = "other"

            # Conditionally adapt question routes according to targeted funding use cases
            if purpose_category == "expand_business":
                business_type = st.selectbox(
                    "Business Type", ["startup", "expand_business"]
                )
                business_duration = st.selectbox(
                    "Business Duration", BUSINESS_DURATION_OPTIONS
                )
            elif purpose_category == "payment":
                payment_type = st.selectbox("Payment Type", LOAN_PURPOSE_OPTIONS)

        with purpose_col2:
            application_frequency = st.selectbox(
                "Application Frequency", APPLICATION_FREQUENCY_OPTIONS
            )
            has_savings = st.selectbox("Has Savings", ["yes", "no"], index=0)
            assets = st.multiselect("Owned Assets", ASSET_OPTIONS, default=[])

    # Pass local scope tracking variables context cleanly out back into parent model thread execution
    return locals()
