import streamlit as st
from src.config.settings import *


def render_old_user_form(POSITION_OPTIONS_BY_EMPLOYMENT):
    """
    Renders the data input tab grouping configured for existing, returning client risk scoring.
    Focuses structural weighting on previous loan performance metrics, repayment patterns,
    financial indicators, and transaction history profiles.
    """
    st.markdown(
        '<div class="panel-title">Existing Customer Assessment</div>',
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Behavior", "Debt", "Trends", "Activity", "Stability"]
    )

    # --- PART 1: REPAYMENT BEHAVIOR (Primary Weight: 35%) ---
    with tab1:
        st.subheader("Repayment Behavior History")
        st.markdown("_Evaluates past payment discipline and borrowing behavior_")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Payment Performance**")
            on_time_payment_rate = st.selectbox(
                "On-Time Payment Rate", ON_TIME_PAYMENT_OPTIONS
            )
            max_dpd = st.selectbox("Maximum DPD (Days Past Due)", MAX_DPD_OPTIONS)
            partial_payment_freq = st.selectbox(
                "Partial Payment Frequency", PARTIAL_PAYMENT_OPTIONS
            )

        with col2:
            st.markdown("**Repayment Patterns**")
            early_repayment = st.selectbox(
                "Early Repayment Frequency", EARLY_REPAYMENT_OPTIONS
            )
            good_borrower_streak = st.selectbox(
                "Good Borrower Streak", ["3+", "1-2", "0"]
            )

        with col3:
            st.markdown("**Credit Utilization**")
            loan_cycle_count = st.number_input("Loan Cycle Count", 0, 20, 1)
            reborrow_frequency = st.selectbox(
                "Reborrow Frequency", REBORROW_FREQUENCY_OPTIONS
            )

    # --- PART 2: DEBT EXPOSURE & FINANCIAL RATIOS (Weight: 30%) ---
    with tab2:
        st.subheader("Debt Exposure Analysis")
        st.markdown("_Assesses current debt levels and capacity_")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Income & Expenses**")
            monthly_income = st.number_input("Monthly Income ($)", 0.0, 500000.0, 500.0)
            income_source_diversity = st.selectbox(
                "Income Sources", INCOME_SOURCE_OPTIONS
            )
            monthly_outflow = st.number_input(
                "Monthly Outflow ($)", 0.0, 500000.0, 300.0
            )

        with col2:
            st.markdown("**Existing Debt**")
            existing_loan_count = st.number_input("Active Loans", 0, 10, 1)
            total_debt_amount = st.number_input(
                "Total Outstanding Debt ($)", 0.0, 500000.0, 150.0
            )
            monthly_debt_payment = st.number_input(
                "Monthly Debt Payment ($)", 0.0, 500000.0, 0.0
            )

        with col3:
            st.markdown("**New Loan Details**")
            loan_amount_str = st.selectbox(
                "Loan Amount ($)", LOAN_AMOUNT_OLD_USER_OPTIONS
            )
            loan_amount = float(loan_amount_str.replace("$", ""))
            loan_tenure = st.selectbox(
                "Loan Tenure (days)", LOAN_TENURE_OPTIONS, index=3
            )

        # Dynamic live evaluation summary calculation definitions
        net_cash_flow_val = monthly_income - monthly_outflow
        expense_ratio_decimal = (
            (monthly_outflow / monthly_income) if monthly_income > 0 else 0.0
        )
        expense_ratio_percent = expense_ratio_decimal * 100
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

        m1, m2, m3, m4, m5, m6 = st.columns(6)
        with m1:
            st.metric("Monthly Income", f"${monthly_income:,.0f}")
        with m2:
            st.metric("Net Cash Flow", f"${net_cash_flow_val:,.0f}")
        with m3:
            st.metric("DTI Ratio", f"{dti_ratio:.1%}")
        with m4:
            st.metric("LTI Ratio", f"{lti_ratio:.1%}")
        with m5:
            st.metric("Affordability Ratio", f"{affordability_ratio:.1%}")
        with m6:
            st.metric("Surplus Income", f"${surplus_income:,.0f}")

    # --- PART 3: FINANCIAL TRENDS DIRECTION (Weight: 10%) ---
    with tab3:
        st.subheader("Financial Trends")
        st.markdown("_Analyzes income, spending, and savings patterns_")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Income Trend**")
            income_trend_direction = st.selectbox(
                "Income Direction", ["Increasing", "Stable", "Decreasing"]
            )
            if income_trend_direction == "Increasing":
                income_change = st.selectbox(
                    "Income Growth", ["> 10%", "5 - 10%", "1 - 5%"]
                )
            elif income_trend_direction == "Decreasing":
                income_change = st.selectbox(
                    "Income Decline", ["> 10%", "5 - 10%", "1 - 5%"]
                )
            else:
                income_change = "Stable"

        with col2:
            st.markdown("**Spending Trend**")
            spending_trend_direction = st.selectbox(
                "Spending Direction", ["Increasing", "Stable", "Decreasing"]
            )
            if spending_trend_direction == "Increasing":
                spending_change = st.selectbox(
                    "Spending Growth", ["> 10%", "5 - 10%", "1 - 5%"]
                )
            elif spending_trend_direction == "Decreasing":
                spending_change = st.selectbox(
                    "Spending Decline", ["> 10%", "5 - 10%", "1 - 5%"]
                )
            else:
                spending_change = "Stable"

        with col3:
            st.markdown("**Savings Trend**")
            savings_trend_direction = st.selectbox(
                "Savings Direction", ["Increasing", "Stable", "Decreasing"]
            )
            if savings_trend_direction == "Increasing":
                savings_change = st.selectbox(
                    "Savings Growth", ["> 10%", "5 - 10%", "1 - 5%"]
                )
            elif savings_trend_direction == "Decreasing":
                savings_change = st.selectbox(
                    "Savings Decline", ["> 10%", "5 - 10%", "1 - 5%"]
                )
            else:
                savings_change = "Stable"

    # --- PART 4: SYSTEM CREDIT ACTIVITY (Weight: 15%) ---
    with tab4:
        st.subheader("Credit Activity")
        st.markdown("_Reviews borrowing frequency and loan purpose_")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Loan Purpose**")
            purpose_category = st.selectbox(
                "Purpose Category", ["expand_business", "payment", "other"]
            )
            business_type = "startup"
            business_duration = None
            payment_type = "other"

            if purpose_category == "expand_business":
                business_type = st.selectbox(
                    "Business Type", ["startup", "expand_business"]
                )
                business_duration = st.selectbox(
                    "Business Duration", BUSINESS_DURATION_OPTIONS
                )
            elif purpose_category == "payment":
                payment_type = st.selectbox("Payment Type", LOAN_PURPOSE_OPTIONS)

        with col2:
            st.markdown("**Loan Structure**")
            loan_tenure_old = st.selectbox("Loan Tenure", LOAN_TENURE_OPTIONS, index=3)
            guarantee_support = st.selectbox("Guarantee Support", ["yes", "no"])

        with col3:
            st.markdown("**Application Behavior**")
            application_frequency = st.selectbox(
                "Application Frequency", APPLICATION_FREQUENCY_OPTIONS
            )

    # --- PART 5: OCCUPATIONAL STABILITY & RETENTION (Weight: 15%) ---
    with tab5:
        st.subheader("Stability & Tenure")
        st.markdown("_Assesses employment and life stability_")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Demographics**")
            age = st.number_input("Age", 18, 100, 40)
            marital_status = st.selectbox("Marital Status", MARITAL_OPTIONS, index=1)
            dependents = st.number_input("Dependents", 1, 10, 1)

        with col2:
            st.markdown("**Employment Profile**")
            employment_type = st.selectbox(
                "Employment Type", EMPLOYMENT_TYPE_OPTIONS, index=1
            )
            position_options = POSITION_OPTIONS_BY_EMPLOYMENT.get(
                employment_type, POSITION_OPTIONS
            )
            position = st.selectbox("Position", position_options)
            employment_tenure = st.selectbox(
                "Employment Tenure", EMPLOYMENT_TENURE_OPTIONS
            )
            work_experience = st.selectbox("Work Experience", WORK_EXPERIENCE_OPTIONS)

        with col3:
            st.markdown("**Living Situation**")
            residence_type = st.selectbox("Residence Type", RESIDENCE_OPTIONS, index=1)
            living_duration = st.selectbox("Living Duration", LIVING_DURATION_OPTIONS)

        st.subheader("Identity & Fraud Verification")

        col1, col2 = st.columns(2)
        with col1:
            face_match = st.selectbox(
                "Face Match with ID", ["matched", "not matched"], index=0
            )
            phone_number_age = st.selectbox(
                "Phone Number Age", PHONE_AGE_OPTIONS, index=2
            )
            employment_verified = st.selectbox(
                "Employment Verified", ["yes", "no"], index=0
            )
        with col2:
            social_linked = st.selectbox(
                "Social Linked Accounts", SOCIAL_LINKS_OPTIONS, index=1
            )
            nid_check = "valid"
            st.success("National ID Verified")

    st.markdown("---")

    # Pack local parameters state to be extracted into parent context upon invocation
    return locals()
