import streamlit as st


def render_global_styles():
    st.markdown(
        """
<style>
    :root {
        --brand-blue: #2563eb;
        --brand-blue-dark: #1d4ed8;
        --ink: #111827;
        --muted: #64748b;
        --line: #e5e7eb;
        --page: #f6f8fb;
    }
    html, body, [data-testid="stAppViewContainer"] {
        background: var(--page);
    }
    [data-testid="stHeader"] {
        background: transparent;
    }
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid var(--line);
        box-shadow: 8px 0 24px rgba(15, 23, 42, 0.04);
    }
    .block-container {
        max-width: 1220px;
        padding-top: 1.2rem !important;
        padding-bottom: 1.25rem !important;
    }
    .hero-header{
        text-align:center;
        margin-bottom:25px;
    }
    .hero-title{
        font-size:48px;
        font-weight:800;
        color:#0f172a;
    }
    .hero-subtitle{
        font-size:20px;
        color:#64748b;
        margin-top:8px;
    }
    .section-header {
        font-size: 1.05rem;
        color: var(--ink);
        font-weight: 700;
        margin-top: 0.25rem;
        margin-bottom: 0.75rem;
    }
    .section-callout {
        color: var(--muted);
        font-size: 0.9rem;
        line-height: 1.5;
        margin-bottom: 1rem;
    }
    .stButton>button {
        border-radius: 8px;
        background-color: var(--brand-blue);
        color: white;
        border: none;
        padding: 0.68rem 0.95rem;
        box-shadow: 0 8px 18px rgba(37, 99, 235, 0.18);
        font-weight: 700;
    }
    .stButton>button:hover {
        background-color: var(--brand-blue-dark);
        color: #ffffff;
    }
    div[data-testid="stButton"] > button {
    height: 55px;
    }
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] {
        border-radius: 8px;
        border: 0 !important;
        min-height: 2.65rem;
        background: #ffffff !important;
        color: #0f172a !important;
        box-shadow:
            inset 0 0 0 1.5px #cbd5e1,
            0 1px 2px rgba(15, 23, 42, 0.04) !important;
        box-sizing: border-box;
        overflow: visible;
    }
    [data-testid="stTextInput"] div:has(> input),
    [data-testid="stNumberInput"] div:has(> input),
    [data-testid="stTextInput"] > div > div,
    [data-testid="stNumberInput"] > div > div {
        min-height: 2.65rem !important;
        border-radius: 8px !important;
        background: #ffffff !important;
        box-shadow:
            inset 0 0 0 2px #bfccd9,
            0 1px 2px rgba(15, 23, 42, 0.05) !important;
    }
    [data-testid="stWidgetLabel"] label,
    [data-testid="stWidgetLabel"] p {
        color: #334155 !important;
        font-weight: 700 !important;
        font-size: 0.86rem !important;
    }
    .panel-title {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        color: var(--ink);
        font-size: 1.08rem;
        font-weight: 800;
        margin: 0 0 0.95rem;
    }
    .card-container, div[data-testid="stMetric"] {
        background: #ffffff;
        border-radius: 8px;
        padding: 1rem 1.1rem;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.04);
        border: 1px solid var(--line);
        margin-bottom: 0.9rem;
    }
    .secondary-text {
        color: var(--muted);
        font-size: 0.92rem;
    }
    .profile-table {
        display: grid;
        gap: 0.6rem;
        color: #334155;
        font-size: 0.9rem;
    }
    .profile-row {
        display: grid;
        grid-template-columns: 140px minmax(0, 1fr);
        gap: 0.8rem;
    }
    .profile-row strong {
        color: var(--muted);
        font-weight: 700;
    }
    .nid-button-pad {
        height: 1.72rem;
    }

/* Hide + and - buttons from number inputs */
[data-testid="stNumberInput"] button {
    display: none !important;
}

[data-testid="stNumberInput"] [role="button"] {
    display: none !important;
}

[data-testid="stNumberInput"] input {
    padding-right: 0 !important;
}

</style>
""",
        unsafe_allow_html=True,
    )
