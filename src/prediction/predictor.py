import pandas as pd
import numpy as np
from src.config.settings import NUMERIC_FEATURES
from .model_loader import preprocess_new, preprocess_old, models

def normalize_input_value(value, is_numeric=False):
    """Convert input value to the appropriate type."""
    if value is None:
        return np.nan
    if isinstance(value, str) and not value.strip():
        return np.nan

    if is_numeric:
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"yes", "y", "true", "t", "1"}:
                return 1.0
            if normalized in {"no", "n", "false", "f", "0"}:
                return 0.0
        try:
            return float(value)
        except (ValueError, TypeError):
            return np.nan

    if isinstance(value, (list, tuple)):
        return ", ".join(str(v) for v in value) if value else np.nan

    return str(value)


def build_input_record(raw_columns, user_input):
    record = {}
    for col in raw_columns:
        is_numeric = col in NUMERIC_FEATURES

        if col in user_input:
            value = user_input[col]
            # Extract numeric part if it's a string like "$50" or "< 3 months"
            if is_numeric and isinstance(value, str):
                numeric_str = ''.join(c for c in value if c.isdigit() or c == '.')
                if numeric_str:
                    try:
                        record[col] = float(numeric_str)
                    except ValueError:
                        record[col] = normalize_input_value(value, is_numeric)
                else:
                    record[col] = normalize_input_value(value, is_numeric)
            else:
                record[col] = normalize_input_value(value, is_numeric)
        else:
            record[col] = np.nan

    return pd.DataFrame([record])


def get_preprocessor_columns(preprocessor):
    if preprocessor is None:
        raise Exception("Prediction resources are not loaded. Check model and preprocessor files.")

    if hasattr(preprocessor, "feature_names_in_") and preprocessor.feature_names_in_ is not None:
        return list(preprocessor.feature_names_in_)
    if hasattr(preprocessor, "get_feature_names_out"):
        return list(preprocessor.get_feature_names_out())
    return []


def predict_default(user_input, user_type, model_choice, threshold):
    try:
        preprocessor = preprocess_new if user_type == "new" else preprocess_old
        if preprocessor is None or models is None:
            raise Exception("Prediction resources are not loaded. Check model and preprocessor files.")

        raw_columns = get_preprocessor_columns(preprocessor)
        X = build_input_record(raw_columns, user_input)
        X_processed = preprocessor.transform(X)
        
        if hasattr(X_processed, "toarray"):
            X_processed = X_processed.toarray()

        expected_features = models[user_type][model_choice].n_features_in_
        if X_processed.shape[1] != expected_features:
            raise Exception(
                f"Prediction error: Preprocessor output has {X_processed.shape[1]} features, "
                f"but {model_choice} is expecting {expected_features} features as input."
            )

        if model_choice == "Ensemble":
            probabilities = [
                model.predict_proba(X_processed)[:, 1][0]
                for model in models[user_type].values()
            ]
            prob = float(np.mean(probabilities))
        else:
            prob = float(models[user_type][model_choice].predict_proba(X_processed)[:, 1][0])

        # Determine risk level
        if prob >= threshold:
            prediction = "High Risk"
        elif prob >= threshold * 0.5:
            prediction = "Medium Risk"
        else:
            prediction = "Low Risk"
        
        return prob, prediction
    except Exception as e:
        raise Exception(f"Prediction error: {str(e)}")