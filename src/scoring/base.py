from src.config.settings import NUMERIC_FEATURES


def normalize_numeric(value):
    try:
        if value is None or value == "":
            return 0.0
        return float(value)
    except Exception:
        return 0.0


def score_range(value, buckets):
    for condition, score, reason in buckets:
        try:
            if condition(value):
                return score, reason
        except Exception:
            continue
    return 0, "No matching rule"


def score_choice(value, mapping, default_reason="No matching rule"):
    key = str(value).strip().lower()
    return mapping.get(key, (0, default_reason))


def normalize_to_fico(raw_score, min_score=0, max_score=100):
    """
    Convert raw rule-based score into FICO-like score (300–850)
    First scales 0-100 range to 0-100 composite
    Then scales to FICO 300-850 range
    """
    raw_score = max(min_score, min(raw_score, max_score))  # clamp to 0-100
    # Scale from 0-100 to FICO 300-850 range
    fico_score = 300 + (raw_score / 100.0) * (850 - 300)
    return round(fico_score)


def calculate_weighted_score(detailed_breakdown, user_type):
    """
    Calculate weighted composite score from detailed breakdown
    Apply component weights and return 0-100 composite score
    """
    try:
        if user_type == "new":
            # NEW USER weights
            weights = {
                "💰 Part 1: Capacity (30%)": 0.30,
                "📊 Part 2: Debt Exposure (28%)": 0.28,
                "🏠 Part 3: Stability (15%)": 0.15,
                "🔐 Part 4: Identity & Fraud (10%)": 0.10,
                "💳 Part 5: Credit Seeking (10%)": 0.10,
                "💎 Part 6: Financial Profile (7%)": 0.07,
            }
        else:
            # OLD USER weights
            weights = {
                "📈 Part 1: Repayment Behavior (35%)": 0.35,
                "📊 Part 2: Debt Exposure (30%)": 0.30,
                "📉 Part 3: Financial Trends (10%)": 0.10,
                "💳 Part 4: Credit Activity (15%)": 0.15,
                "🏠 Part 5: Stability (15%)": 0.15,
            }

        total_weighted_score = 0.0
        total_weight = 0.0

        for component, features in detailed_breakdown.items():
            # Calculate average score for this component (scale each feature to 0-5, then to 0-100)
            component_scores = [f.get("score", 0) for f in features.values()]

            if component_scores:
                # Normalize each score to 0-5 range if needed
                # Most scores are already in -5 to 5 range, convert to 0-100
                # Map -5 to 5 range to 0 to 100: (score + 5) / 10 * 100
                normalized_scores = []
                for score in component_scores:
                    # Convert from -5 to 5 range to 0 to 100 range
                    normalized = ((score + 5) / 10) * 100
                    normalized = max(0, min(100, normalized))  # clamp to 0-100
                    normalized_scores.append(normalized)

                component_avg = sum(normalized_scores) / len(normalized_scores)
                component_weight = weights.get(component, 0)
                if component_weight == 0:
                    component_weight = next(
                        (
                            weight
                            for name, weight in weights.items()
                            if component in name
                        ),
                        0,
                    )
                total_weighted_score += component_avg * component_weight
                total_weight += component_weight

        # Normalize to 0-100 scale
        if total_weight > 0:
            composite_score = total_weighted_score / total_weight
        else:
            composite_score = 50.0

        return composite_score

    except Exception as e:
        return 50.0


def fico_category(fico_score):
    if fico_score >= 800:
        return "Excellent"
    elif fico_score >= 740:
        return "Very Good"
    elif fico_score >= 670:
        return "Good"
    elif fico_score >= 580:
        return "Fair"
    else:
        return "Poor"


def final_credit_score(raw_score):
    fico_score = normalize_to_fico(raw_score)
    category = fico_category(fico_score)

    return {"fico_score": fico_score, "category": category}


def final_credit_score_from_breakdown(detailed_breakdown, user_type):
    """
    Calculate FICO score from detailed breakdown with proper weighting
    """
    composite_score = calculate_weighted_score(detailed_breakdown, user_type)
    fico_score = normalize_to_fico(composite_score)
    category = fico_category(fico_score)

    return {
        "fico_score": fico_score,
        "category": category,
        "composite_score": round(composite_score, 2),
    }
