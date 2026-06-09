import sys
from pathlib import Path

import streamlit as st
import pandas as pd
import numpy as np

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from src.ui.helpers import parse_int_value, parse_percentage, show_nid_popup
from src.config.settings import *
from src.database.db_manager import DemoDBManager
from src.scoring.utils import *
from src.prediction.predictor import predict_default
from src.prediction.model_loader import load_resources
from src.ui.components import render_global_styles

# Import separated modules
from src.ui.pages.new_user_form import render_new_user_form
from src.ui.pages.old_user_form import render_old_user_form
from src.ui.pages.history import render_assessment_history

# Dictionary defining dynamic options routing to map professional titles to specific employment streams
POSITION_OPTIONS_BY_EMPLOYMENT = {
    "Business Owner": ["Founder", "Co-Founder"],
    "Government Officer": [
        "Officer",
        "Deputy Head of Department",
        "Director",
        "Head of Department",
        "Other",
    ],
    "Employee": ["Staff", "Worker", "Senior Manager", "Manager", "Other"],
    "Other": POSITION_OPTIONS,
}

# Configure Streamlit main view dashboard geometry parameters
st.set_page_config(
    page_title="AI-Based Credit Scoring System",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply global unified custom CSS stylesheet definitions
render_global_styles()

# --- HARDWARE & RESOURCE LOADING ---
# Load trained Machine Learning model serialized artifacts and preprocessing pipeline instances
preprocess_new, preprocess_old, models = load_resources()
if preprocess_new is None or preprocess_old is None or models is None:
    st.error(
        "Unable to load prediction resources. "
        "Please verify the model and preprocessor files in the demo/model and demo/preprocess folders."
    )
    st.stop()

# Initialize active tracking fields in state to avoid reset exceptions across execution reruns
if "existing_user_id" not in st.session_state:
    st.session_state["existing_user_id"] = None
if "user_type" not in st.session_state:
    st.session_state["user_type"] = "new"

# ============================================================================
# SIDEBAR CONTROL INTERFACE
# ============================================================================
with st.sidebar:
    # Top-level application routing switch
    page = st.radio(
        "Navigation",
        [
            "Credit Assessment",
            "Assessment History",
        ],
    )
    user_type = st.session_state.get("user_type", "new")
    industry_type = st.session_state.get("industry_type", None)
    position = st.session_state.get("position", None)

    # Core Machine Learning variant selection dropdown menu mapping to available system types
    model_choice = st.selectbox(
        "Prediction Model",
        ["RF", "LR", "SVM", "MLP"],
        format_func=lambda value: {
            "RF": "Random Forest (RF)",
            "LR": "Logistic Regression (LR)",
            "SVM": "Support Vector Machine (SVM)",
            "MLP": "Neural Network (MLP)",
        }.get(value, value),
        help="Choose the ML model for prediction",
    )

    # Probability classification threshold adjustment boundary slider
    threshold = st.slider(
        "Decision Threshold",
        0.0,
        1.0,
        0.5,
        help="Adjust the default probability threshold",
    )

    # National ID verification submission interface blocks
    n_id_col, check_col = st.columns([2.25, 0.9])
    with n_id_col:
        n_id = st.text_input("National ID")
    with check_col:
        st.markdown('<div class="nid-button-pad"></div>', unsafe_allow_html=True)
        check_nid = st.button("Check", key="check_nid")

    # Present diagnostic status messages based on NID verification state tracking
    if "nid_status" in st.session_state:
        if st.session_state.get("user_type") == "old":
            st.success(st.session_state["nid_status"])
        else:
            st.info(st.session_state["nid_status"])

    # Execution path triggering database query lookups for returning applicant matching
    if check_nid:
        if not n_id:
            st.warning("Please enter a National ID before checking.")
        else:
            db = DemoDBManager()
            if db.connect():
                try:
                    existing_user = db.get_user_by_nid(n_id.strip())
                    if existing_user:
                        # Existing applicant identified - update state and configure system to load historical mode
                        st.session_state["existing_user_id"] = existing_user["user_id"]
                        st.session_state["user_type"] = "old"
                        st.session_state["first_name"] = existing_user.get(
                            "first_name", ""
                        )
                        st.session_state["last_name"] = existing_user.get(
                            "last_name", ""
                        )
                        st.session_state["gender"] = existing_user.get("gender", "")
                        st.session_state["nid_status"] = (
                            f"NID found. Existing customer identified."
                        )
                        st.rerun()
                    else:
                        # Clear state data for unregistered inputs - routing workflow to a New User Form path
                        st.session_state["existing_user_id"] = None
                        st.session_state["user_type"] = "new"
                        st.session_state["first_name"] = ""
                        st.session_state["last_name"] = ""
                        st.session_state["gender"] = "Male"
                        st.session_state["nid_status"] = (
                            "No existing NID found. This will be treated as a new user."
                        )
                        st.rerun()
                finally:
                    db.disconnect()
            else:
                st.error("Unable to connect to the database to verify NID.")

    # Shared generic applicant identity fields
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input(
            "First Name", value=st.session_state.get("first_name", "")
        )
    with col2:
        last_name = st.text_input(
            "Last Name", value=st.session_state.get("last_name", "")
        )
    gender = st.selectbox(
        "Gender",
        GENDER_OPTIONS,
        index=GENDER_OPTIONS.index(st.session_state.get("gender", "Male")),
    )
    relationship_with_platform = st.selectbox(
        "Relationship with Platform", RELATIONSHIP_OPTIONS
    )

# Render common application title block layout structures on screen
st.markdown(
    """
<div class="hero-header">
    <div class="hero-title">Loan Decision Support System</div>
    <div class="hero-subtitle">Credit risk evaluation and loan decisions</div>
</div>
""",
    unsafe_allow_html=True,
)

# --- APPLICATION NAVIGATIONAL DISPATCH ROUTER ---
if page == "Assessment History":
    render_assessment_history()
    st.stop()  # Stop structural layout thread processing to bypass evaluation forms completely

# Render specialized entry form variants matching targeted profile tracking flags
if user_type == "new":
    form_data = render_new_user_form(
        first_name,
        last_name,
        gender,
        relationship_with_platform,
        POSITION_OPTIONS_BY_EMPLOYMENT,
        n_id,
    )
else:
    form_data = render_old_user_form(POSITION_OPTIONS_BY_EMPLOYMENT)

# Unpack dictionary keys into primary namespace context variables for pipeline calculation access
locals().update(form_data)

# ============================================================================
# EVALUATION & PIPELINE PREDICTION PROCESSING
# ============================================================================
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown(
        '<div class="secondary-text">Review the profile and run the assessment when all required information is complete.</div>',
        unsafe_allow_html=True,
    )
with col2:
    predict_button = st.button("Prediction", use_container_width=True, key="predict")

if predict_button:
    missing_fields = []

    # Mandatory input validation constraints checks
    if not n_id or len(n_id.strip()) == 0:
        show_nid_popup()

    if not first_name or len(first_name.strip()) == 0:
        missing_fields.append("First Name")

    if not last_name or len(last_name.strip()) == 0:
        missing_fields.append("Last Name")

    if missing_fields:
        st.error(
            "Please complete the following required fields:\n\n• "
            + "\n• ".join(missing_fields)
        )
        st.stop()

    try:
        # Build comprehensive mapping data payload to ensure model alignment structures
        input_data = {
            "monthly_income": monthly_income,
            "monthly_outflow": (
                monthly_outflow if "monthly_outflow" in locals() else 0.0
            ),
            "income_source_diversity": (
                income_source_diversity
                if "income_source_diversity" in locals()
                else "1 source"
            ),
            "expense_ratio": (
                expense_ratio_decimal if "expense_ratio_decimal" in locals() else 0.5
            ),
            "net_cash_flow": (
                net_cash_flow_val if "net_cash_flow_val" in locals() else 0.0
            ),
            "guarantee_support": (
                guarantee_support if "guarantee_support" in locals() else "no"
            ),
            "loan_amount": loan_amount if "loan_amount" in locals() else 0.0,
            "loan_tenure": (
                loan_tenure
                if "loan_tenure" in locals()
                else (loan_tenure_old if "loan_tenure_old" in locals() else 30)
            ),
            "existing_loan_count": (
                existing_loan_count if "existing_loan_count" in locals() else 0
            ),
            "total_debt_amount": (
                total_debt_amount if "total_debt_amount" in locals() else 0.0
            ),
            "monthly_debt_payment": (
                monthly_debt_payment if "monthly_debt_payment" in locals() else 0.0
            ),
            "surplus_income": surplus_income if "surplus_income" in locals() else 0.0,
            "dti_ratio": dti_ratio if "dti_ratio" in locals() else 0.0,
            "lti_ratio": lti_ratio if "lti_ratio" in locals() else 0.0,
            "affordability_ratio": (
                affordability_ratio if "affordability_ratio" in locals() else 0.0
            ),
            "age": age if "age" in locals() else 0,
            "marital_status": (
                marital_status if "marital_status" in locals() else "single"
            ),
            "education_level": (
                education_level if "education_level" in locals() else "Other"
            ),
            "living_duration": (
                living_duration if "living_duration" in locals() else "1-2 years"
            ),
            "residence_type": (
                residence_type if "residence_type" in locals() else "rent"
            ),
            "employment_type": (
                employment_type if "employment_type" in locals() else "other"
            ),
            "employment_tenure": (
                employment_tenure if "employment_tenure" in locals() else "1-2 years"
            ),
            "work_experience": (
                work_experience if "work_experience" in locals() else "< 1 year"
            ),
            "industry": industry_type if "industry_type" in locals() else "Other",
            "position": position if "position" in locals() else "Other",
            "face_match": face_match if "face_match" in locals() else "not matched",
            "employment_verified": (
                employment_verified if "employment_verified" in locals() else "no"
            ),
            "social_linked": social_linked if "social_linked" in locals() else "0",
            "nid_check": nid_check if "nid_check" in locals() else "invalid",
            "application_frequency": (
                application_frequency
                if "application_frequency" in locals()
                else "1/quarter"
            ),
            "loan_purpose": (
                payment_type
                if "purpose_category" in locals() and purpose_category == "payment"
                else (
                    business_type
                    if "purpose_category" in locals()
                    and purpose_category == "expand_business"
                    else purpose_category if "purpose_category" in locals() else "other"
                )
            ),
            "asset_ownership": (
                ", ".join(assets) if "assets" in locals() and assets else np.nan
            ),
            "saving_indicator": (
                1 if "has_savings" in locals() and has_savings == "yes" else 0
            ),
            "is_urban": 1 if "is_urban" in locals() and is_urban == "Yes" else 0,
            "has_savings": has_savings if "has_savings" in locals() else "no",
            "assets": assets if "assets" in locals() else [],
            "income_trend_direction": (
                income_trend_direction
                if "income_trend_direction" in locals()
                else "Stable"
            ),
            "spending_trend_direction": (
                spending_trend_direction
                if "spending_trend_direction" in locals()
                else "Stable"
            ),
            "savings_trend_direction": (
                savings_trend_direction
                if "savings_trend_direction" in locals()
                else "Stable"
            ),
            "loan_cycle_count": (
                loan_cycle_count if "loan_cycle_count" in locals() else 1
            ),
            "reborrow_frequency": (
                reborrow_frequency if "reborrow_frequency" in locals() else "7-30 days"
            ),
            "on_time_payment_rate": (
                on_time_payment_rate if "on_time_payment_rate" in locals() else None
            ),
            "on_time_payment_ratio": (
                parse_percentage(on_time_payment_rate)
                if "on_time_payment_rate" in locals()
                else None
            ),
            "max_dpd": parse_int_value(max_dpd) if "max_dpd" in locals() else None,
            "early_repayment": (
                early_repayment if "early_repayment" in locals() else None
            ),
            "early_repayment_count": (
                parse_int_value(early_repayment)
                if "early_repayment" in locals()
                else None
            ),
            "good_borrower_streak": (
                good_borrower_streak if "good_borrower_streak" in locals() else None
            ),
            "partial_payment_freq": (
                partial_payment_freq if "partial_payment_freq" in locals() else None
            ),
            "partial_payment": (
                partial_payment_freq if "partial_payment_freq" in locals() else None
            ),
        }

        # Invoke core classification models returning computed structural results
        probability, label = predict_default(
            input_data, user_type, model_choice, threshold
        )

        # Hard guard checks analyzing validation structural safety flags
        identity_issues = []
        if face_match == "not matched":
            identity_issues.append("Face not matched with ID")
        if nid_check != "valid":
            identity_issues.append("National ID verification failed")

        if identity_issues:
            st.markdown("---")
            st.header("Identity Verification Result")
            if len(identity_issues) >= 2 or label == "Default":
                st.error(
                    "## APPLICATION REJECTED\n\n**Reason:** Identity verification failed"
                )
                for issue in identity_issues:
                    st.error(f"• {issue}")
                st.error(
                    "**Status:** User not verified - Cannot proceed with assessment"
                )
            else:
                st.warning(
                    "## APPLICATION REVIEW REQUIRED\n\n**Reason:** Identity verification issues detected"
                )
            st.stop()

        # Display structured result statistics layout panels
        st.markdown("---")
        st.header("Assessment Results")

        col1, col2, col3 = st.columns([1.2, 1, 1.3])
        with col1:
            if label == "High Risk":
                st.error(f"Risk: {label}")
            elif label == "Low Risk":
                st.success(f"Risk: {label}")
            else:
                st.warning(f"Risk: {label}")
        with col2:
            st.metric("Default Probability", f"{probability:.1%}")
        with col3:
            # Generate weighted matrix scoring breakdown elements based on structural logic configs
            detailed_breakdown = calculate_score_breakdown(input_data, user_type)
            fico_score = final_credit_score_from_breakdown(
                detailed_breakdown, user_type
            )
            st.metric(
                "Overall Scoring",
                f"{fico_score['fico_score']}",
                f"{fico_score['category']}",
            )

        st.divider()
        st.subheader("Detailed Scoring Breakdown - All Features")

        # Map and present score grids for user transparency checks across metric groupings
        for component, features in detailed_breakdown.items():
            with st.expander(f"**{component}**", expanded=True):
                feature_data = []
                for feature_name, feature_info in features.items():
                    feature_data.append(
                        {
                            "Feature": feature_name,
                            "Score": feature_info.get("score", 0),
                            "Rating": feature_info.get("reason", ""),
                            "Value": feature_info.get("value", "N/A"),
                        }
                    )
                feature_df = pd.DataFrame(feature_data)
                st.dataframe(feature_df, use_container_width=True, hide_index=True)

        st.subheader("Risk Assessment Details")
        if label == "High Risk":
            recommendation = "REJECT"
            recommendation_color = "error"
            recommendation_detail = (
                "High probability of default. Loan application is not recommended."
            )
        elif label == "Low Risk":
            recommendation = "APPROVE"
            recommendation_color = "success"
            recommendation_detail = (
                "Strong credit profile with low probability of default."
            )
        else:
            recommendation = "REVIEW"
            recommendation_color = "warning"
            recommendation_detail = "Moderate risk profile- Requires further review"

        col1, col2 = st.columns(2)
        with col1:
            st.info(
                f"- **User Type:** {user_type.upper()}\n- **Model:** {model_choice}\n- **Threshold:** {threshold:.2f}"
            )
        with col2:
            st.info(
                f"- **Default Risk:** {label}\n- **Probability:** {probability:.2%}\n- **Recommendation:** {recommendation}"
            )

        st.markdown("---")
        if recommendation_color == "error":
            st.error(f"## {recommendation}\n{recommendation_detail}")
        elif recommendation_color == "success":
            st.success(f"## {recommendation}\n{recommendation_detail}")
        else:
            st.warning(f"## {recommendation}\n{recommendation_detail}")

        # ============================================================================
        # DATABASE LOGGING PIPELINE SECTION
        # ============================================================================
        try:
            db = DemoDBManager()
            if db.connect():
                existing_user_id = st.session_state.get("existing_user_id")

                # Assemble normalized schemas for transactional storage
                user_data = {
                    "n_id": n_id or None,
                    "user_type": user_type,
                    "first_name": first_name or "Unknown",
                    "last_name": last_name or "Unknown",
                    "age": age,
                    "gender": gender,
                    "marital_status": marital_status,
                    "dependents": dependents,
                    "education_level": (
                        education_level if "education_level" in locals() else None
                    ),
                    "employment_type": (
                        employment_type if "employment_type" in locals() else None
                    ),
                    "employment_tenure": (
                        employment_tenure if "employment_tenure" in locals() else None
                    ),
                    "business_creation_time": (
                        business_creation_time
                        if "business_creation_time" in locals()
                        else None
                    ),
                    "work_experience": work_experience,
                    "industry_type": (
                        industry_type if "industry_type" in locals() else None
                    ),
                    "position": position if "position" in locals() else None,
                    "residence_type": residence_type,
                    "living_duration": living_duration,
                    "geo_is_urban": (
                        True if "is_urban" in locals() and is_urban == "Yes" else False
                    ),
                    "relationship_with_platform": relationship_with_platform,
                    "loan_cycle_count": (
                        loan_cycle_count if "loan_cycle_count" in locals() else 1
                    ),
                }

                financial_data = {
                    "monthly_income": monthly_income,
                    "income_source_diversity": (
                        parse_int_value(income_source_diversity)
                        if "income_source_diversity" in locals()
                        else None
                    ),
                    "monthly_outflow": monthly_outflow,
                    "expense_ratio": expense_ratio_decimal,
                    "net_cash_flow": net_cash_flow_val,
                    "monthly_debt_payment": monthly_debt_payment,
                    "surplus_income": surplus_income,
                    "saving_indicator": (
                        True
                        if "has_savings" in locals() and has_savings == "yes"
                        else False
                    ),
                    "guarantee_support": (
                        True
                        if "guarantee_support" in locals()
                        and guarantee_support
                        in ["yes", "Strong (3)", "Very Strong (4)", "Excellent (5)"]
                        else False
                    ),
                    "asset_ownership": (
                        ", ".join(assets) if "assets" in locals() else None
                    ),
                    "income_stability_trend": (
                        income_trend_direction
                        if "income_trend_direction" in locals()
                        else None
                    ),
                    "spending_trend": (
                        spending_trend_direction
                        if "spending_trend_direction" in locals()
                        else None
                    ),
                    "saving_trend": (
                        savings_trend_direction
                        if "savings_trend_direction" in locals()
                        else None
                    ),
                }

                loan_data = {
                    "loan_amount": loan_amount,
                    "loan_tenure": loan_tenure,
                    "loan_purpose": (
                        purpose_category if "purpose_category" in locals() else None
                    ),
                    "existing_loan_count": existing_loan_count,
                    "total_debt_amount": total_debt_amount,
                    "dti_ratio": dti_ratio,
                    "lti_ratio": lti_ratio,
                    "affordability_ratio": affordability_ratio,
                    "application_frequency": application_frequency,
                }

                identity_data = {
                    "id_verification_status": (
                        "Verified"
                        if face_match == "matched" and nid_check in ["valid"]
                        else "Unverified"
                    ),
                    "phone_number_age": phone_number_age,
                    "employment_application": (
                        employment_verified
                        if "employment_verified" in locals()
                        else None
                    ),
                    "social_media_link_account": (
                        social_linked if "social_linked" in locals() else None
                    ),
                    "nid_check": nid_check if "nid_check" in locals() else None,
                }

                score_data = {
                    "final_credit_score": fico_score.get("fico_score"),
                    "risk_level": label,
                    "approval_status": (
                        "APPROVED"
                        if label == "Low Risk"
                        else "REVIEW" if label == "Medium Risk" else "REJECTED"
                    ),
                }

                prediction_data = {
                    "default_probability": probability * 100,
                    "prediction_label": label,
                    "model_used": model_choice,
                }

                repayment_data = None
                if user_type == "old":
                    repayment_data = {
                        "on_time_payment_rate": parse_percentage(on_time_payment_rate),
                        "max_dpd": parse_int_value(max_dpd),
                        "early_repayment_count": parse_int_value(early_repayment),
                        "good_borrower_streak": parse_int_value(good_borrower_streak),
                        "partial_payment": partial_payment_freq,
                        "loan_cycle_count": loan_cycle_count,
                        "reborrow_frequency": reborrow_frequency,
                    }

                # Commit structured payload transaction to storage schemas via DB Manager pipeline
                saved = db.save_assessment(
                    user_data=user_data,
                    financial_data=financial_data,
                    loan_data=loan_data,
                    identity_data=identity_data,
                    score_data=score_data,
                    prediction_data=prediction_data,
                    repayment_data=repayment_data,
                    existing_user_id=existing_user_id,
                )

                if saved:
                    st.success("Assessment saved to the credit_system database")
                else:
                    st.warning(
                        "Could not save to the database. Check connection and schema setup."
                    )
            else:
                st.warning("Unable to connect to the credit_system database.")
        except Exception as db_err:
            st.error(f"Database error: {db_err}")
        finally:
            if "db" in locals():
                db.disconnect()

    except Exception as e:
        st.error(f"Error during prediction: {str(e)}")
        st.info("Please ensure all fields are properly filled")
