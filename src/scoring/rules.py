from .base import score_range, score_choice, normalize_numeric


def score_monthly_income(value):
    return score_range(
        value,
        [
            (lambda x: x > 500, 5, "Very strong income"),
            (lambda x: x > 400, 4, "Good income"),
            (lambda x: x > 300, 3, "Normal income"),
            (lambda x: x > 200, 2, "Low income"),
            (lambda x: x >= 0, 1, "Very weak income"),
        ],
    )


def score_loan_amount(value):
    return score_range(
        value,
        [
            (lambda x: x <= 50, 5, "Lowest loan exposure"),
            (lambda x: x <= 100, 3, "Moderate loan exposure"),
            (lambda x: x <= 150, 1, "High loan exposure"),
            (lambda x: x > 150, -2, "Very high loan exposure"),
        ],
    )


def score_expense_ratio(value):
    return score_range(
        value,
        [
            (lambda x: x < 0.50, 5, "Low expense burden"),
            (lambda x: x < 0.56, 4, "Manageable expenses"),
            (lambda x: x < 0.61, 3, "Moderate expenses"),
            (lambda x: x < 0.66, 2, "Higher expense burden"),
            (lambda x: x < 0.71, 1, "High expense burden"),
            (lambda x: x >= 0.71, -5, "Very high expense burden"),
        ],
    )


def score_net_cash_flow(value):
    return score_range(
        value,
        [
            (lambda x: x > 0, 5, "Positive net cash flow"),
            (lambda x: x == 0, 3, "Break-even cash flow"),
            (lambda x: x < 0, -5, "Negative cash flow"),
        ],
    )


def score_guarantee_support(value):
    mapping = {
        "yes": (5, "Guarantee provided"),
        "no": (0, "No guarantee"),
    }
    return score_choice(value, mapping, (0, "No guarantee"))


def score_dti_ratio(value):
    return score_range(
        value,
        [
            (lambda x: x < 0.25, 5, "Very low debt-to-income"),
            (lambda x: x <= 0.35, 4, "Good debt-to-income"),
            (lambda x: x <= 0.50, 3, "Moderate debt-to-income"),
            (lambda x: x <= 0.59, 2, "High debt-to-income"),
            (lambda x: x > 0.59, -5, "Very high debt-to-income"),
        ],
    )


def score_lti_ratio(value):
    return score_range(
        value,
        [
            (lambda x: x < 0.25, 5, "Very low loan-to-income"),
            (lambda x: x <= 0.50, 3, "Manageable loan-to-income"),
            (lambda x: x <= 0.75, 1, "Moderate loan burden"),
            (lambda x: x <= 1.0, -2, "High loan burden"),
            (lambda x: x > 1.0, -5, "Severe over-borrowing"),
        ],
    )


def score_exist_loans(value):
    return score_range(
        value,
        [
            (lambda x: x == 0, 5, "No existing loans"),
            (lambda x: x == 1, 3, "One existing loan"),
            (lambda x: x >= 2, 2, "Multiple loans"),
        ],
    )


def score_total_debt_ratio(value, income):
    if income <= 0:
        return 0, "Income missing for debt ratio"
    ratio = value / income
    return score_range(
        ratio,
        [
            (lambda x: x < 0.1, 5, "Very low debt burden"),
            (lambda x: x < 0.2, 4, "Healthy debt level"),
            (lambda x: x < 0.35, 3, "Moderate leverage"),
            (lambda x: x < 0.5, 1, "High leverage"),
            (lambda x: x >= 0.5, -3, "Critical leverage"),
        ],
    )


def score_affordability_ratio(value):
    return score_range(
        value,
        [
            (lambda x: x < 0.30, 5, "Very low affordability pressure"),
            (lambda x: x < 0.50, 3, "Manageable affordability pressure"),
            (lambda x: x >= 0.50, -5, "Very high affordability pressure"),
        ],
    )

def score_surplus_income(value):
    return score_range(
        value,
        [
            (lambda x: x >= 300, 5, "Strong repayment capacity"),
            (lambda x: x >= 200, 4, "Good surplus income"),
            (lambda x: x >= 100, 3, "Moderate surplus income"),
            (lambda x: x >= 50, 2, "Limited surplus income"),
            (lambda x: x >= 0, 1, "Very low surplus income"),
            (lambda x: x < 0, -5, "Negative surplus income"),
        ],
    )
    
def score_monthly_debt_payment(value, income):
    if income <= 0:
        return 0, "Income unavailable"

    ratio = value / income

    return score_range(
        ratio,
        [
            (lambda x: x < 0.10, 5, "Very low debt burden"),
            (lambda x: x < 0.20, 4, "Low debt burden"),
            (lambda x: x < 0.30, 3, "Manageable debt burden"),
            (lambda x: x < 0.40, 2, "Elevated debt burden"),
            (lambda x: x < 0.50, 1, "High debt burden"),
            (lambda x: x >= 0.50, -5, "Critical debt burden"),
        ],
    )
    
def score_loan_tenure(value):
    return score_range(
        value,
        [
            (lambda x: x >= 120, 5, "Long repayment tenor"),
            (lambda x: x >= 90, 4, "Good repayment tenor"),
            (lambda x: x >= 60, 3, "Moderate repayment tenor"),
            (lambda x: x >= 30, 2, "Short repayment tenor"),
            (lambda x: x < 30, 1, "Very short repayment tenor"),
        ],
    )


def score_on_time_payment_ratio(value):
    return score_range(
        value,
        [
            (lambda x: x >= 0.95, 5, "Excellent repayment discipline"),
            (lambda x: x >= 0.85, 4, "Good repayment discipline"),
            (lambda x: x >= 0.70, 3, "Average repayment discipline"),
            (lambda x: x >= 0.50, 2, "Weak repayment discipline"),
            (lambda x: x < 0.50, -3, "Very poor repayment discipline"),
        ],
    )


def score_max_dpd(value):
    return score_range(
        value,
        [
            (lambda x: x == 0, 5, "No late payments"),
            (lambda x: x <= 15, 3, "Minor delinquency"),
            (lambda x: x > 15, -5, "High delinquency risk"),
        ],
    )


def score_early_repayment_count(value):
    if value >= 5:
        return 5, "Very strong early repayment" 
    if value == 4:
        return 4, "Strong early repayment" 
    if value == 3:
        return 3, "Good early repayment" 
    if value == 2:
        return 2, "Moderate early repayment" 
    if value == 1:
        return 1, "Low early repayment" 
    return 0, "No early repayment history"


def score_loan_cycle_count(value):
    return score_range(
        value,
        [
            (lambda x: x >= 4, 5, "Experienced borrower"),
            (lambda x: x >= 2, 3, "Moderate borrowing experience"),
            (lambda x: x == 1, 1, "New borrower"),
            (lambda x: x <= 0, 0, "Missing loan cycle history"),
        ],
    )


def score_income_source_diversity(value):
    """Score income source diversity"""
    mapping = {
        "3+ sources": (5, "Very stable income from multiple sources"),
        "2 sources": (4, "Fairly stable income with backup source"),
        "1 source": (2, "Risky single income source"),
    }
    return score_choice(value, mapping, (2, "Single income source"))


def score_marital_status(value):
    """Score marital status"""
    mapping = {
        "married": (5, "More stable life situation"),
        "single": (3, "Normal stability"),
        "divorced": (2, "Possible financial instability"),
    }
    return score_choice(value, mapping, (3, "Unknown status"))


def score_dependents_count(value):
    """Score number of dependents"""
    value = normalize_numeric(value)
    if value == 0:
        return 5, "Full income available for repayment"
    elif value == 1:
        return 3, "Manageable but reduces disposable income"
    elif value == 2:
        return 2, "Noticeable impact on cash flow"
    elif value == 3:
        return 1, "Limited flexibility for repayment"
    else:
        return 0, "Strong financial pressure"


def score_residence_type(value):
    """Score residence type"""
    mapping = {
        "self-owned": (5, "Very stable living situation"),
        "parent's": (4, "Stable but dependent"),
        "rented": (3, "Moderate stability"),
        "sibling": (2, "Less stable"),
        "company": (2, "Less stable"),
    }
    return score_choice(value, mapping, (0, "Unknown residence"))


def score_living_duration(value):
    """Score living duration"""
    mapping = {
        "< 3 months": (-2, "Very unstable residence"),
        "less than 3 months": (-2, "Very unstable residence"),
        "< 6 months": (-1, "Early-stage residence"),
        "less than 6 months": (-1, "Early-stage residence"),
        "< 1 year": (0, "Basic stability"),
        "less than 1 year": (0, "Basic stability"),
        "1-2 years": (1, "Improving stability"),
        "1 - 2 years": (1, "Improving stability"),
        "2-3 years": (2, "Strong residential stability"),
        "2 - 3 years": (2, "Strong residential stability"),
        "> 3 years": (3, "Very stable residence"),
        "more than 3 years": (3, "Very stable residence"),
    }
    return score_choice(value, mapping, (0, "Unknown duration"))


def score_employment_type(value):
    """Score employment type"""
    mapping = {
        "government officer": (5, "Very stable job"),
        "government": (5, "Very stable job"),
        "employee": (4, "Stable job"),
        "business owner": (3, "Income may vary"),
        "business": (3, "Income may vary"),
        "other": (2, "Variable employment"),
    }
    return score_choice(value, mapping, (0, "Unknown employment"))


def score_employment_tenure(value):
    """Score employment tenure"""
    mapping = {
        "> 3 years": (5, "Very strong job stability"),
        "1 - 3 years": (4, "Good job stability"),
        "1-3 years": (4, "Good job stability"),
        "6 - 12 months": (3, "Medium stability"),
        "6-12 months": (3, "Medium stability"),
        "3 - 6 months": (2, "Weak stability"),
        "3-6 months": (2, "Weak stability"),
        "< 3 months": (1, "Very new job"),
    }
    return score_choice(value, mapping, (2, "Unknown tenure"))


def score_work_experience(value):
    """Score work experience"""
    mapping = {
        "> 9 years": (5, "Very strong experience"),
        "6 - 9 years": (4, "Good experience"),
        "6-9 years": (4, "Good experience"),
        "3 - 6 years": (3, "Moderate experience"),
        "3-6 years": (3, "Moderate experience"),
        "1 - 3 years": (2, "Limited experience"),
        "1-3 years": (2, "Limited experience"),
        "< 1 year": (1, "Very low experience"),
    }
    return score_choice(value, mapping, (1, "Unknown experience"))


def score_education_level(value):
    """Score education level"""
    mapping = {
        "phd": (5, "Very high education"),
        "master": (4, "High education"),
        "bachelor": (3, "Standard education"),
        "high school": (2, "Basic education"),
        "other": (1, "Low education"),
    }
    return score_choice(value, mapping, (2, "Unknown education"))


def score_phone_number_age(value):
    """Score phone number age"""
    mapping = {
        "> 5 years": (5, "Long-term phone ownership"),
        "> 4 years": (3, "Stable phone history"),
        "> 3 years": (2, "Moderate phone history"),
        "> 1.5 years": (1, "Limited phone history"),
        "< 1.5 years": (0, "Very recent phone"),
        ">5 years": (5, "Long-term phone ownership"),
        ">4 years": (3, "Stable phone history"),
        ">3 years": (2, "Moderate phone history"),
        ">1.5 years": (1, "Limited phone history"),
        "<1.5 years": (0, "Very recent phone"),
    }
    return score_choice(value, mapping, (0, "Unknown age"))


def score_partial_payment_frequency(value):
    """Score partial payment frequency for old users"""
    mapping = {
        "> 50%": (0, "Very frequent partial payments"),
        "> 40%": (1, "High partial payment frequency"),
        "> 30%": (2, "Moderate partial payment"),
        "> 20%": (3, "Acceptable level"),
        "> 10%": (4, "Low partial payment"),
        "< 10%": (5, "Very rare partial payments"),
        ">50%": (0, "Very frequent partial payments"),
        ">40%": (1, "High partial payment frequency"),
        ">30%": (2, "Moderate partial payment"),
        ">20%": (3, "Acceptable level"),
        ">10%": (4, "Low partial payment"),
        "<10%": (5, "Very rare partial payments"),
    }
    return score_choice(value, mapping, (2, "Unknown frequency"))


def score_reborrow_frequency(value):
    """Score reborrow frequency"""
    mapping = {
        ">30 days": (5, "Healthy borrowing behavior"),
        "7-30 days": (3, "Normal borrowing"),
        "<7 days": (1, "Too frequent borrowing"),
        "> 30 days": (5, "Healthy borrowing behavior"),
        "< 7 days": (1, "Too frequent borrowing"),
    }
    return score_choice(value, mapping, (2, "Unknown"))


def score_id_verification_status(value):
    return score_choice(value, {"verified": (5, "Identity verified"), "unverified": (0, "Identity not verified")}, (0, "Unknown verification"))


def score_employment_application(value):
    return score_choice(value, {"yes": (5, "Employment verified"), "no": (0, "Unverified employment")}, (0, "Unknown employment verification"))


def score_social_linked(value):
    mapping = {
        "3": (3, "Multiple verified accounts"),
        "2": (2, "Some linked accounts"),
        "1": (1, "Only one linked"),
        "0": (0, "No linked accounts"),
        "3+ accounts": (3, "Multiple verified accounts"),
        "2 accounts": (2, "Some linked accounts"),
        "1 account": (1, "Only one linked"),
        "none": (0, "No linked accounts"),
    }
    return score_choice(value, mapping, (0, "No linked accounts"))


def score_business_duration(value):
    mapping = {
        "< 3 months": (0, "Very new business"),
        "< 6 month": (1, "Early-stage business"),
        "< 12 months": (2, "Developing business"),
        "< 24 months": (3, "Established business"),
        "< 30 months": (4, "Mature business"),
        "> 30 months": (5, "Long-running/proven business"),
    }
    return score_choice(value, mapping, (0, "Unknown business duration"))


def score_payment_type(value):
    mapping = {
        "expand_business": (5, "Income-generating purpose"),
        "payment": (4, "Essential need"),
        "livelihood support": (4, "Essential loan purpose"),
        "living expense": (4, "Essential loan purpose"),
        "repair of the house": (4, "Essential loan purpose"),
        "vehicles": (4, "Productive asset purchase"),
        "medical treatment": (3, "Necessary expense"),
        "travel": (2, "Non-essential travel"),
        "shopping": (-3, "Discretionary spending"),
        "wedding": (2, "Social expense"),
        "bill payment services": (3, "Essential service payment"),
        "other": (0, "Unclear purpose"),
    }
    return score_choice(value, mapping, (0, "Unknown purpose"))


def score_application_frequency(value):
    mapping = {
        "1/month": (5, "Normal borrowing"),
        "2/month": (3, "Slightly higher activity"),
        "3+": (-5, "Frequent/stressed borrowing"),
        "<1/year": (5, "Very low borrowing frequency"),
        "1/year": (4, "Low borrowing frequency"),
        "1/quarter": (3, "Moderate borrowing frequency"),
        "2+/month": (1, "High borrowing frequency"),
    }
    return score_choice(value, mapping, (3, "Unknown frequency"))


def score_savings(value):
    return score_choice(value, {"yes": (5, "Shows financial discipline"), "no": (0, "No reserve fund")}, (0, "Unknown savings"))


def score_asset_ownership(assets):
    if not assets:
        return 0, "No major assets"
    mapping = {"car": 5, "motobike": 4, "motorbike": 4, "phone": 2, "computer": 3}
    score = 0
    for asset in assets:
        score = max(score, mapping.get(str(asset).strip().lower(), 0))
    reason = "Owns asset(s)" if score > 0 else "No major assets"
    return score, reason


def score_industry_type(value):
    """Score industry type as a proxy for business stability."""
    mapping = {
        "business": (4, "Business activity with steady demand"),
        "building": (4, "Construction/building with regular contracts"),
        "service": (3, "Service sector with moderate stability"),
        "delivery": (3, "Delivery/logistics with variable demand"),
        "other": (2, "Unknown/variable industry stability"),
    }
    return score_choice(value, mapping, (2, "Unknown industry"))


def score_position(value):
    """Score job position / role to reflect income/stability level."""
    mapping = {
        "worker": (2, "Basic role with lower salary and less stability"),
        "skilled worker": (3, "Skilled role with better stability"),
        "staff": (4, "Office role with regular salary"),
        "officer": (4, "Office role with regular salary"),
        "senior manager": (5, "Senior role with high stability and income"),
        "manager": (5, "Manager role with high stability and income"),
        "co-founder": (5, "Founder-level role with strong commitment"),
        "director": (5, "Executive role with strong stability"),
        "founder": (4, "Founder/owner with variable stability"),
        "other": (2, "Unknown role stability"),
    }
    return score_choice(value, mapping, (2, "Unknown position"))


