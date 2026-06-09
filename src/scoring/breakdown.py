from . import base
from .rules import *

def is_yes(value):
    if isinstance(value, (int, float)):
        return int(value) == 1
    return str(value).strip().lower() == "yes"

def _display_raw(values, key, formatted):
    """Prefer showing the raw user input for a key when available, otherwise use formatted string."""
    if key in values and values.get(key) is not None:
        return values.get(key)
    return formatted


def _parse_percentage_value(val):
    """Parse a percentage-like input into a float between 0 and 1.
    Accepts numeric input (0.3), strings like '> 40%', '40%', '>=95%'."""
    try:
        if val is None:
            return None
        if isinstance(val, (int, float)):
            # assume already 0-1 or whole number percentage >1
            if val > 1:
                return float(val) / 100.0
            return float(val)
        s = str(val)
        # extract first number
        import re
        m = re.search(r"(\d+\.?\d*)", s)
        if m:
            num = float(m.group(1))
            # if given as percent like 40 or '40%'
            if '%' in s or num > 1:
                return num / 100.0
            return num
    except Exception:
        pass
    return None


def _parse_int_value(val):
    """Parse an integer-like input from strings like '1 - 15 days' or numeric types."""
    try:
        if val is None:
            return None
        if isinstance(val, int):
            return val
        if isinstance(val, float):
            return int(val)
        s = str(val)
        import re
        m = re.search(r"(\d+)", s)
        if m:
            return int(m.group(1))
    except Exception:
        pass
    return None

def calculate_score_breakdown(values, user_type):
    """Calculate detailed score breakdown for ALL features from CSV"""
    try:
        detailed_breakdown = {}
        
        if user_type == "new":
            # NEW USER - 6 PARTS
            
            # Part 1: CAPACITY (30%)
            capacity_features = {}
            monthly_income = base.normalize_numeric(values.get("monthly_income", 1000))
            income_score, income_reason = score_monthly_income(monthly_income)
            capacity_features["Monthly Income"] = {
                "score": income_score,
                "reason": income_reason,
                "value": f"${monthly_income:,.0f}"
            }
            
            income_diversity = values.get("income_source_diversity", "1 source")
            income_div_score, income_div_reason = score_income_source_diversity(income_diversity)
            capacity_features["Income Source Diversity"] = {
                "score": income_div_score,
                "reason": income_div_reason,
                "value": income_diversity
            }
            
            expense_ratio = base.normalize_numeric(values.get("expense_ratio", 0.5))
            expense_score, expense_reason = score_expense_ratio(expense_ratio)
            capacity_features["Expense Ratio"] = {
                "score": expense_score,
                "reason": expense_reason,
                "value": f"{expense_ratio:.1%}"
            }
            
            # Get net_cash_flow - either from values dict or calculate it
            if "net_cash_flow" in values:
                net_cash_flow = base.normalize_numeric(values.get("net_cash_flow", 0))
            else:
                monthly_outflow = base.normalize_numeric(values.get("monthly_outflow", monthly_income * expense_ratio))
                net_cash_flow = monthly_income - monthly_outflow
            
            cash_flow_score, cash_flow_reason = score_net_cash_flow(net_cash_flow)
            capacity_features["Net Cash Flow"] = {
                "score": cash_flow_score,
                "reason": cash_flow_reason,
                "value": f"${net_cash_flow:,.0f}"
            }
            
            guarantee_support = values.get("guarantee_support", "None (0)")
            guarantee_score, guarantee_reason = score_guarantee_support(guarantee_support)
            capacity_features["Guarantee Support"] = {
                "score": guarantee_score,
                "reason": guarantee_reason,
                "value": guarantee_support
            }
            
            detailed_breakdown["Part 1: Capacity"] = capacity_features
            
            # Part 2: DEBT EXPOSURE (28%)
            debt_features = {}
            loan_amount = base.normalize_numeric(values.get("loan_amount", 5000))
            loan_score, loan_reason = score_loan_amount(loan_amount / 1000)  # Convert to thousands
            debt_features["Loan Amount"] = {
                "score": loan_score,
                "reason": loan_reason,
                "value": f"${loan_amount:,.0f}"
            }
            
            total_debt = base.normalize_numeric(values.get("total_debt_amount", 0))
            dti_ratio = (total_debt / monthly_income) if monthly_income > 0 else 0
            dti_score, dti_reason = score_dti_ratio(dti_ratio)
            debt_features["Debt-to-Income Ratio"] = {
                "score": dti_score,
                "reason": dti_reason,
                "value": f"{dti_ratio:.1%}"
            }
            
            lti_ratio = (loan_amount / monthly_income) if monthly_income > 0 else 0
            lti_score, lti_reason = score_lti_ratio(lti_ratio)
            debt_features["Loan-to-Income Ratio"] = {
                "score": lti_score,
                "reason": lti_reason,
                "value": f"{lti_ratio:.1%}"
            }
            
            existing_loans = base.normalize_numeric(values.get("existing_loan_count", 0))
            existing_score, existing_reason = score_exist_loans(existing_loans)
            debt_features["Existing Loans"] = {
                "score": existing_score,
                "reason": existing_reason,
                "value": f"{int(existing_loans)} loans"
            }
            
            total_debt_ratio = (total_debt / monthly_income) if monthly_income > 0 else 0
            total_debt_score, total_debt_reason = score_total_debt_ratio(total_debt, monthly_income)
            debt_features["Total Debt Ratio"] = {
                "score": total_debt_score,
                "reason": total_debt_reason,
                "value": f"{total_debt_ratio:.1%}"
            }
            
            monthly_debt_payment = base.normalize_numeric(values.get("monthly_debt_payment", 0))
            payment_score, payment_reason = score_monthly_debt_payment(monthly_debt_payment, monthly_income)
            debt_features["Monthly Debt Payment"] = {
                "score": payment_score,
                "reason": payment_reason,
                "value": f"${monthly_debt_payment:,.0f}"
            }
            
            surplus_income = base.normalize_numeric(values.get("surplus_income", 0))
            surplus_score, surplus_reason = score_surplus_income(surplus_income)
            debt_features["Surplus Income"] = {
                "score": surplus_score,
                "reason": surplus_reason,
                "value": f"${surplus_income:,.0f}"
            }
            
            
            detailed_breakdown["Part 2: Debt Exposure"] = debt_features
            
            # Part 3: STABILITY (15%)
            stability_features = {}
            age = base.normalize_numeric(values.get("age", 35))
            if 33 <= age <= 44:
                age_score = 5
                age_reason = "Very stable working age"
            elif 25 <= age <= 32:
                age_score = 4
                age_reason = "Stable working age"
            elif 45 <= age <= 55:
                age_score = 3
                age_reason = "Stable but health concerns"
            elif 18 <= age <= 24:
                age_score = 2
                age_reason = "Young with limited experience"
            else:
                age_score = -1
                age_reason = "Age outside optimal range"
            stability_features["Age"] = {
                "score": age_score,
                "reason": age_reason,
                "value": f"{int(age)} years"
            }
            
            marital_status = values.get("marital_status", "single")
            marital_score, marital_reason = score_marital_status(marital_status)
            stability_features["Marital Status"] = {
                "score": marital_score,
                "reason": marital_reason,
                "value": marital_status
            }
            
            dependents = base.normalize_numeric(values.get("dependents", 0))
            dependent_score, dependent_reason = score_dependents_count(dependents)
            stability_features["Dependents"] = {
                "score": dependent_score,
                "reason": dependent_reason,
                "value": f"{int(dependents)}"
            }
            
            residence_type = values.get("residence_type", "rent")
            residence_score, residence_reason = score_residence_type(residence_type)
            stability_features["Residence Type"] = {
                "score": residence_score,
                "reason": residence_reason,
                "value": residence_type
            }
            
            living_duration = values.get("living_duration", "1-2 years")
            living_score, living_reason = score_living_duration(living_duration)
            stability_features["Living Duration"] = {
                "score": living_score,
                "reason": living_reason,
                "value": living_duration
            }
            
            employment_type = values.get("employment_type", "employee")
            employment_type_score, employment_type_reason = score_employment_type(employment_type)
            stability_features["Employment Type"] = {
                "score": employment_type_score,
                "reason": employment_type_reason,
                "value": employment_type
            }
            
            employment_tenure = values.get("employment_tenure", "1-2 years")
            employment_tenure_score, employment_tenure_reason = score_employment_tenure(employment_tenure)
            stability_features["Employment Tenure"] = {
                "score": employment_tenure_score,
                "reason": employment_tenure_reason,
                "value": employment_tenure
            }
            
            work_experience = values.get("work_experience", "3-6 years")
            work_exp_score, work_exp_reason = score_work_experience(work_experience)
            stability_features["Work Experience"] = {
                "score": work_exp_score,
                "reason": work_exp_reason,
                "value": work_experience
            }
            
            education_level = values.get("education_level", "bachelor")
            education_score, education_reason = score_education_level(education_level)
            stability_features["Education Level"] = {
                "score": education_score,
                "reason": education_reason,
                "value": education_level
            }
            
            is_urban = values.get("is_urban", 1)
            urban_score = 4 if is_yes(is_urban) else 3
            urban_reason = "Better access to jobs and services" if urban_score == 4 else "Moderate access"
            stability_features["Urban Location"] = {
                "score": urban_score,
                "reason": urban_reason,
                "value": is_urban
            }

            # Industry type contributes to stability
            industry_type = values.get("industry_type", "Other")
            industry_score, industry_reason = score_industry_type(industry_type)
            stability_features["Industry Type"] = {
                "score": industry_score,
                "reason": industry_reason,
                "value": industry_type
            }

            # Position / role contributes to stability
            position = values.get("position", "Other")
            position_score, position_reason = score_position(position)
            stability_features["Position"] = {
                "score": position_score,
                "reason": position_reason,
                "value": position
            }
            
            detailed_breakdown["Part 3: Stability"] = stability_features
            
            # Part 4: IDENTITY & FRAUD (10%)
            identity_features = {}
            face_match = values.get("face_match", "not matched")
            id_score = 5 if str(face_match).strip().lower() == "matched" else 0
            identity_features["ID Verification"] = {
                "score": id_score,
                "reason": "Identity fully confirmed" if id_score > 0 else "High fraud risk",
                "value": face_match
            }

            phone_age = values.get("phone_number_age", "< 1.5 years")
            phone_score, phone_reason = score_phone_number_age(phone_age)
            identity_features["Phone Number Age"] = {
                "score": phone_score,
                "reason": phone_reason,
                "value": phone_age
            }
            
            employment_verified = values.get("employment_verified", "no")
            employment_score = 5 if is_yes(employment_verified) else 0
            identity_features["Employment Verified"] = {
                "score": employment_score,
                "reason": "Job confirmed" if employment_score > 0 else "Unverified job",
                "value": employment_verified
            }
            
            social_linked = values.get("social_linked", "0")
            social_map = {"3": (3, "Multiple verified accounts"), "2": (2, "Some linked accounts"), "1": (1, "Only one linked"), "0": (0, "No linked accounts")}
            social_score, social_reason = social_map.get(str(social_linked), (0, "No linked accounts"))
            identity_features["Social Linked Accounts"] = {
                "score": social_score,
                "reason": social_reason,
                "value": str(social_linked)
            }
            
            nid_check = values.get("nid_check", "invalid")
            nid_score = 5 if nid_check.lower() in ["valid", "new", "existing"] else 0
            identity_features["National ID Check"] = {
                "score": nid_score,
                "reason": "Valid ID confirmed" if nid_score > 0 else "Invalid or missing ID",
                "value": nid_check
            }
            
            detailed_breakdown["Part 4: Identity & Fraud"] = identity_features
            
            # Part 5: CREDIT SEEKING BEHAVIOR (10%)
            seeking_features = {}
            application_freq = values.get("application_frequency", "1/quarter")
            app_freq_map = {
                "1/month": (5, "Normal borrowing"),
                "2/month": (3, "Slightly higher activity"),
                "3+": (-5, "Frequent/stressed borrowing")
            }
            app_score, app_reason = app_freq_map.get(application_freq, (3, "Unknown frequency"))
            seeking_features["Application Frequency"] = {
                "score": app_score,
                "reason": app_reason,
                "value": application_freq
            }
            
            loan_tenure = base.normalize_numeric(values.get("loan_tenure", 30))
            tenure_score, tenure_reason = score_loan_tenure(loan_tenure)
            seeking_features["Loan Tenure"] = {
                "score": tenure_score,
                "reason": tenure_reason,
                "value": f"{loan_tenure:.0f} days"
            }
            
            purpose_category = values.get("purpose_category", "other")
            payment_type = values.get("payment_type", "other")
            business_type = values.get("business_type")
            if purpose_category == "payment":
                purpose_score, purpose_reason = score_payment_type(payment_type)
                purpose_value = payment_type
            elif purpose_category == "expand_business" and business_type:
                purpose_score, purpose_reason = score_payment_type(purpose_category)
                purpose_value = business_type
            else:
                purpose_score, purpose_reason = score_payment_type(purpose_category)
                purpose_value = purpose_category
            seeking_features["Loan Purpose"] = {
                "score": purpose_score,
                "reason": purpose_reason,
                "value": purpose_value
            }
            
            business_duration = values.get("business_duration", "< 3 months")
            business_score, business_reason = score_business_duration(business_duration)
            seeking_features["Business Duration"] = {
                "score": business_score,
                "reason": business_reason,
                "value": business_duration
            }
            
            detailed_breakdown["Part 5: Credit Seeking"] = seeking_features
            
            # Part 6: FINANCIAL PROFILE (7%)
            profile_features = {}
            has_savings = values.get("has_savings", "no")
            savings_score = 5 if is_yes(has_savings) else 0
            profile_features["Savings"] = {
                "score": savings_score,
                "reason": "Shows financial discipline" if savings_score > 0 else "No reserve fund",
                "value": has_savings
            }
            
            assets = values.get("assets", [])
            if isinstance(assets, str):
                assets = assets.split(",") if assets else []
            assets_map = {"car": 5, "motorbike": 4, "computer": 3, "phone": 2}
            asset_score = 0
            for asset in assets:
                asset_score = max(asset_score, assets_map.get(asset.strip().lower(), 0))
            if asset_score == 0 and assets:
                asset_score = 2
            profile_features["Asset Ownership"] = {
                "score": asset_score,
                "reason": f"Owns {len(assets)} valuable asset(s)" if assets else "No major assets",
                "value": ", ".join(assets) if assets else "None"
            }
            
            detailed_breakdown["Part 6: Financial Profile"] = profile_features
        
        else:  # OLD USER
            # OLD USER - 5 PARTS
            
            # Part 1: REPAYMENT BEHAVIOR (35%)
            behavior_features = {}
            raw_on_time = values.get("on_time_payment_rate", values.get("on_time_payment_ratio", 0.85))
            parsed_on_time = _parse_percentage_value(raw_on_time)
            if parsed_on_time is None:
                parsed_on_time = base.normalize_numeric(values.get("on_time_payment_ratio", 0.85))
            on_time_score, on_time_reason = score_on_time_payment_ratio(parsed_on_time)
            behavior_features["On-Time Payment Rate"] = {
                "score": on_time_score,
                "reason": on_time_reason,
                "value": _display_raw(values, "on_time_payment_rate", f"{parsed_on_time:.1%}")
            }
            
            raw_dpd = values.get("max_dpd", 0)
            parsed_dpd = _parse_int_value(raw_dpd)
            if parsed_dpd is None:
                parsed_dpd = int(base.normalize_numeric(raw_dpd) or 0)
            dpd_score, dpd_reason = score_max_dpd(parsed_dpd)
            behavior_features["Maximum DPD"] = {
                "score": dpd_score,
                "reason": dpd_reason,
                "value": _display_raw(values, "max_dpd", f"{int(parsed_dpd)} days")
            }
            
            # Prefer explicit early_repayment_count for scoring if available
            if "early_repayment_count" in values and values.get("early_repayment_count") is not None:
                cnt = base.normalize_numeric(values.get("early_repayment_count", 0))
                early_score, early_reason = score_early_repayment_count(cnt)
                display_val = _display_raw(values, "early_repayment_count", int(cnt))
            else:
                # fallback to percentage-style input like '> 40%'
                pct_raw = values.get("early_repayment", None)
                pct = _parse_percentage_value(pct_raw)
                if pct is None:
                    pct = 0.0
                # Map percentage to score
                if pct >= 0.5:
                    early_score, early_reason = 5, "Very frequent early repayment"
                elif pct >= 0.4:
                    early_score, early_reason = 4, "High early repayment"
                elif pct >= 0.3:
                    early_score, early_reason = 3, "Good early repayment"
                elif pct >= 0.2:
                    early_score, early_reason = 2, "Moderate early repayment"
                elif pct >= 0.1:
                    early_score, early_reason = 1, "Low early repayment"
                else:
                    early_score, early_reason = 0, "Very rare early repayment"
                display_val = _display_raw(values, "early_repayment", f"{pct:.0%}")

            behavior_features["Early Repayment Frequency"] = {
                "score": early_score,
                "reason": early_reason,
                "value": display_val
            }
            
            good_streak = values.get("good_borrower_streak", "1-2")
            streak_score = {"3+": 5, "1-2": 3, "0": -3}.get(good_streak, 2)
            behavior_features["Good Borrower Streak"] = {
                "score": streak_score,
                "reason": "Consistently good borrower",
                "value": good_streak
            }
            
            partial_payment_freq = values.get("partial_payment_freq", values.get("partial_payment", "< 10%"))
            partial_score, partial_reason = score_partial_payment_frequency(partial_payment_freq)
            behavior_features["Partial Payment Frequency"] = {
                "score": partial_score,
                "reason": partial_reason,
                "value": _display_raw(values, "partial_payment_freq", _display_raw(values, "partial_payment", partial_payment_freq))
            }
            
            loan_cycle_raw = values.get("loan_cycle_count", 1)
            loan_cycle_parsed = _parse_int_value(loan_cycle_raw)
            if loan_cycle_parsed is None:
                loan_cycle_parsed = int(base.normalize_numeric(loan_cycle_raw) or 1)
            loan_cycle = loan_cycle_parsed
            cycle_score, cycle_reason = score_loan_cycle_count(loan_cycle)
            behavior_features["Loan Cycle Count"] = {
                "score": cycle_score,
                "reason": cycle_reason,
                "value": _display_raw(values, "loan_cycle_count", f"{int(loan_cycle)}")
            }
            
            reborrow_freq = values.get("reborrow_frequency", "7-30 days")
            reborrow_score, reborrow_reason = score_reborrow_frequency(reborrow_freq)
            behavior_features["Reborrow Frequency"] = {
                "score": reborrow_score,
                "reason": reborrow_reason,
                "value": _display_raw(values, "reborrow_frequency", reborrow_freq)
            }
            
            detailed_breakdown["Part 1: Repayment Behavior"] = behavior_features
            
            # Part 2: DEBT EXPOSURE (30%)
            debt_features = {}
            monthly_income = base.normalize_numeric(values.get("monthly_income", 2000))
            income_score, income_reason = score_monthly_income(monthly_income)
            debt_features["Monthly Income"] = {
                "score": income_score,
                "reason": income_reason,
                "value": f"${monthly_income:,.0f}"
            }
            
            income_diversity = values.get("income_source_diversity", "1 source")
            income_div_score, income_div_reason = score_income_source_diversity(income_diversity)
            debt_features["Income Source Diversity"] = {
                "score": income_div_score,
                "reason": income_div_reason,
                "value": income_diversity
            }
            
            expense_ratio = base.normalize_numeric(values.get("expense_ratio", 0.5))
            expense_score, expense_reason = score_expense_ratio(expense_ratio)
            debt_features["Expense Ratio"] = {
                "score": expense_score,
                "reason": expense_reason,
                "value": f"{expense_ratio:.1%}"
            }
            
            total_debt = base.normalize_numeric(values.get("total_debt_amount", 5000))
            dti_ratio = (total_debt / monthly_income) if monthly_income > 0 else 0
            dti_score, dti_reason = score_dti_ratio(dti_ratio)
            debt_features["Debt-to-Income Ratio"] = {
                "score": dti_score,
                "reason": dti_reason,
                "value": f"{dti_ratio:.1%}"
            }
            
            monthly_debt_payment = base.normalize_numeric(values.get("monthly_debt_payment", 1000))
            payment_score, payment_reason = score_monthly_debt_payment(monthly_debt_payment, monthly_income)
            debt_features["Monthly Debt Payment"] = {
                "score": payment_score,
                "reason": payment_reason,
                "value": f"${monthly_debt_payment:,.0f}"
            }
            
            surplus_income = base.normalize_numeric(values.get("surplus_income", 500))
            surplus_score, surplus_reason = score_surplus_income(surplus_income)
            debt_features["Surplus Income"] = {
                "score": surplus_score,
                "reason": surplus_reason,
                "value": f"${surplus_income:,.0f}"
            }
            
            existing_loans = base.normalize_numeric(values.get("existing_loan_count", 1))
            existing_score, existing_reason = score_exist_loans(existing_loans)
            debt_features["Active Loans"] = {
                "score": existing_score,
                "reason": existing_reason,
                "value": f"{int(existing_loans)}"
            }
            
            detailed_breakdown["Part 2: Debt Exposure"] = debt_features
            
            # Part 3: FINANCIAL TRENDS (10%)
            trends_features = {}
            income_trend = values.get("income_trend_direction", "Stable")
            income_trend_score = 5 if income_trend == "Increasing" else (3 if income_trend == "Stable" else 1)
            trends_features["Income Trend"] = {
                "score": income_trend_score,
                "reason": "Income improving" if income_trend_score > 2 else "Income declining",
                "value": income_trend
            }
            
            spending_trend = values.get("spending_trend_direction", "Stable")
            spending_trend_score = 5 if spending_trend == "Decreasing" else (3 if spending_trend == "Stable" else 1)
            trends_features["Spending Trend"] = {
                "score": spending_trend_score,
                "reason": "Spending controlled" if spending_trend_score > 2 else "Spending increasing",
                "value": spending_trend
            }
            
            savings_trend = values.get("savings_trend_direction", "Stable")
            savings_trend_score = 5 if savings_trend == "Increasing" else (3 if savings_trend == "Stable" else 1)
            trends_features["Savings Trend"] = {
                "score": savings_trend_score,
                "reason": "Savings growing" if savings_trend_score > 2 else "Savings declining",
                "value": savings_trend
            }
            
            detailed_breakdown["Part 3: Financial Trends"] = trends_features
            
            # Part 4: CREDIT ACTIVITY (15%)
            activity_features = {}
            application_freq = values.get("application_frequency", "1/quarter")
            app_score = {"<1/year": 5, "1/year": 4, "1/quarter": 3, "1/month": 2, "2+/month": 1}.get(application_freq, 3)
            activity_features["Application Frequency"] = {
                "score": app_score,
                "reason": "Stable borrowing pattern",
                "value": application_freq
            }
            
            loan_cycle = base.normalize_numeric(values.get("loan_cycle_count", 1))
            cycle_score, cycle_reason = score_loan_cycle_count(loan_cycle)
            activity_features["Loan Cycle Count"] = {
                "score": cycle_score,
                "reason": cycle_reason,
                "value": f"{int(loan_cycle)}"
            }
            
            reborrow_freq = values.get("reborrow_frequency", "Regular")
            reborrow_score = 5 if reborrow_freq == "Regular" else (3 if reborrow_freq == "Occasional" else 1)
            activity_features["Reborrow Frequency"] = {
                "score": reborrow_score,
                "reason": "Consistent borrower" if reborrow_score >= 3 else "Irregular borrower",
                "value": reborrow_freq
            }
            
            detailed_breakdown["Part 4: Credit Activity"] = activity_features
            
            # Part 5: STABILITY (15%)
            stability_features = {}
            age = base.normalize_numeric(values.get("age", 40))
            if 30 <= age <= 60:
                age_score = 5
                age_reason = "Optimal working age"
            elif 18 <= age <= 65:
                age_score = 3
                age_reason = "Acceptable age range"
            else:
                age_score = 1
                age_reason = "Outside optimal range"
            stability_features["Age"] = {
                "score": age_score,
                "reason": age_reason,
                "value": f"{int(age)} years"
            }
            
            employment_type = values.get("employment_type", "employee")
            employment_type_score, employment_type_reason = score_employment_type(employment_type)
            stability_features["Employment Type"] = {
                "score": employment_type_score,
                "reason": employment_type_reason,
                "value": employment_type
            }
            
            employment_tenure = values.get("employment_tenure", "2-5 years")
            employment_tenure_score, employment_tenure_reason = score_employment_tenure(employment_tenure)
            stability_features["Employment Tenure"] = {
                "score": employment_tenure_score,
                "reason": employment_tenure_reason,
                "value": employment_tenure
            }
            
            work_experience = values.get("work_experience", "3-6 years")
            work_exp_score, work_exp_reason = score_work_experience(work_experience)
            stability_features["Work Experience"] = {
                "score": work_exp_score,
                "reason": work_exp_reason,
                "value": work_experience
            }
            
            living_duration = values.get("living_duration", "2-5 years")
            living_score, living_reason = score_living_duration(living_duration)
            stability_features["Living Duration"] = {
                "score": living_score,
                "reason": living_reason,
                "value": living_duration
            }
            
            marital_status = values.get("marital_status", "married")
            marital_score, marital_reason = score_marital_status(marital_status)
            stability_features["Marital Status"] = {
                "score": marital_score,
                "reason": marital_reason,
                "value": marital_status
            }
            
            dependents = base.normalize_numeric(values.get("dependents", 1))
            dependent_score, dependent_reason = score_dependents_count(dependents)
            stability_features["Dependents"] = {
                "score": dependent_score,
                "reason": dependent_reason,
                "value": f"{int(dependents)}"
            }

            # Industry and position for old users also affect stability
            industry_type = values.get("industry_type", "Other")
            industry_score, industry_reason = score_industry_type(industry_type)
            stability_features["Industry Type"] = {
                "score": industry_score,
                "reason": industry_reason,
                "value": industry_type
            }

            position = values.get("position", "Other")
            position_score, position_reason = score_position(position)
            stability_features["Position"] = {
                "score": position_score,
                "reason": position_reason,
                "value": position
            }
            
            detailed_breakdown["Part 5: Stability"] = stability_features
        
        return detailed_breakdown
    
    except Exception as e:
        # Fallback default breakdown
        return {
            "Summary": {
                "Error": {
                    "score": 0,
                    "reason": str(e),
                    "value": "Error occurred"
                }
            }
        }
