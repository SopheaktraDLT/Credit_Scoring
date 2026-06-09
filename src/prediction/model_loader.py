import streamlit as st
import joblib
from pathlib import Path

# Project root: credit_scoring/
BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_DIR = BASE_DIR / "model"
PREPROCESS_DIR = BASE_DIR / "preprocessor"


@st.cache_resource
def load_resources():
    try:
        preprocess_new = joblib.load(
            PREPROCESS_DIR / "new_user" / "new_preprocessor.pkl"
        )

        preprocess_old = joblib.load(
            PREPROCESS_DIR / "old_user" / "old_preprocessor.pkl"
        )

        models = {
            "new": {
                "RF": joblib.load(MODEL_DIR / "new_user" / "NEW_RF.pkl"),
                "LR": joblib.load(MODEL_DIR / "new_user" / "NEW_LR.pkl"),
                "SVM": joblib.load(MODEL_DIR / "new_user" / "NEW_SVM.pkl"),
                "MLP": joblib.load(MODEL_DIR / "new_user" / "NEW_MLP.pkl"),
            },
            "old": {
                "RF": joblib.load(MODEL_DIR / "old_user" / "OLD_RF.pkl"),
                "LR": joblib.load(MODEL_DIR / "old_user" / "OLD_LR.pkl"),
                "SVM": joblib.load(MODEL_DIR / "old_user" / "OLD_SVM.pkl"),
                "MLP": joblib.load(MODEL_DIR / "old_user" / "OLD_MLP.pkl"),
            },
        }

        return preprocess_new, preprocess_old, models

    except Exception as e:
        st.error(f"Error loading models or preprocessors: {e}")
        return None, None, None


preprocess_new, preprocess_old, models = load_resources()
