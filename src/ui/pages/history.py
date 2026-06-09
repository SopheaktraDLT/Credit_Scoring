import streamlit as st
import pandas as pd
import math
from src.database.db_manager import DemoDBManager


def render_assessment_history():
    """
    Renders the Assessment History dashboard panel.
    Fetches loan evaluation historical logs from the database, displays key performance
    indicators (KPI metrics), applies search filters, and displays records in a paginated table.
    """
    st.title("Assessment History Dashboard")
    db = DemoDBManager()

    # Establish a reliable connection to the credit database
    if db.connect():
        try:
            # SQL query joining core system tables (users, loan_information, credit_scoring, prediction_result)
            # The CASE statement checks if a loan record is the oldest entry for a user to flag applicant type.
            query = """
            SELECT
                li.loan_id,
                u.user_id,
                CASE
                    WHEN li.loan_id = (
                        SELECT MIN(li2.loan_id)
                        FROM loan_information li2
                        WHERE li2.user_id = u.user_id
                    )
                    THEN 'New User Applicant'
                    ELSE 'Old User Applicant'
                END AS applicant_type,
                u.n_id,
                CONCAT(u.first_name,' ',u.last_name) AS customer_name,
                cs.final_credit_score,
                cs.risk_level,
                cs.approval_status,
                pr.default_probability
            FROM users u
            LEFT JOIN loan_information li
                ON u.user_id = li.user_id
            LEFT JOIN credit_scoring cs
                ON u.user_id = cs.user_id
            LEFT JOIN prediction_result pr
                ON u.user_id = pr.user_id
            ORDER BY li.loan_id DESC"""

            # Read query results into a pandas DataFrame
            df = pd.read_sql(query, db.connection)

            # Ensure table clean-up by removing duplicate active loan references, preserving the latest state
            df.drop_duplicates(subset=["loan_id"], keep="last", inplace=True)

            # User input box to capture text patterns matching National Identity or Applicant Names
            search = st.text_input("Search by NID or Name")

            # Apply strict presentation formats for raw database values
            df["loan_id"] = df["loan_id"].apply(
                lambda x: f"LN{x:05d}" if pd.notnull(x) else "-"
            )
            df["default_probability"] = df["default_probability"].fillna(0).round(2)

            # Rename technical system columns into human-readable table headers
            df = df.rename(
                columns={
                    "loan_id": "Loan ID",
                    "user_id": "User ID",
                    "n_id": "NID",
                    "applicant_type": "Applicant Type",
                    "customer_name": "Customer Name",
                    "final_credit_score": "Credit Score",
                    "risk_level": "Risk Level",
                    "approval_status": "Approval Status",
                    "default_probability": "Default Probability",
                }
            )

            # Select and organize columns explicitly matching the historical grid architecture
            df = df[
                [
                    "Loan ID",
                    "Applicant Type",
                    "NID",
                    "Customer Name",
                    "Credit Score",
                    "Risk Level",
                    "Default Probability",
                    "Approval Status",
                ]
            ]

            # Column structure splitting search functionality: main text field and confirmation button
            col_s1, col_s2 = st.columns([5, 1])
            with col_s1:
                if search:
                    # Filter dataset based on partial case-insensitive string matches for Name or NID
                    df = df[
                        df["Customer Name"]
                        .astype(str)
                        .str.contains(search, case=False, na=False)
                        | df["NID"]
                        .astype(str)
                        .str.contains(search, case=False, na=False)
                    ]
            with col_s2:
                search_btn = st.button("Search", use_container_width=True)

            # Calculate and display the 5 high-level dashboard metrics cards
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Total Customers", len(df))
            with col2:
                st.metric(
                    "Old Applicants",
                    len(df[df["Applicant Type"] == "Old User Applicant"]),
                )
            with col3:
                st.metric("Average Score", f"{df['Credit Score'].fillna(0).mean():.0f}")
            with col4:
                st.metric("Approved", len(df[df["Approval Status"] == "APPROVED"]))
            with col5:
                st.metric("Rejected", len(df[df["Approval Status"] == "REJECTED"]))

            # Inject customized style overrides ensuring strict alignment for functional buttons
            st.markdown(
                """
                <style>
                    div[data-testid="stButton"] button {
                        height: 38px;
                        min-height: 38px;
                        padding: 0 12px;
                        border-radius: 8px;
                        font-size: 14px;
                    }
                </style>
                """,
                unsafe_allow_html=True,
            )

            # --- PAGINATION CALCULATIONS ---
            rows_per_page = 10

            # Initialize active page configuration tracking variable inside session state
            if "page_num" not in st.session_state:
                st.session_state.page_num = 1

            total_rows = len(df)
            total_pages = max(1, math.ceil(total_rows / rows_per_page))

            # Guard against out-of-bounds selection ranges due to changes in filtering
            if st.session_state.page_num > total_pages:
                st.session_state.page_num = total_pages

            current_page = st.session_state.page_num

            # Slice current dataframe into explicit viewable segments matching selected limits
            start_idx = (current_page - 1) * rows_per_page
            end_idx = start_idx + rows_per_page
            page_df = df.iloc[start_idx:end_idx]

            # Render the resulting segmented table view on screen
            st.dataframe(
                page_df,
                use_container_width=True,
                hide_index=True,
            )

            # --- PAGINATION NAVIGATION INTERFACE ---
            left_space, center, right_space = st.columns([4, 3, 4])

            with center:
                cols = st.columns([0.8, 0.8, 2.5, 0.8, 0.8])

                # Navigate back to the absolute starting index (Page 1)
                with cols[0]:
                    if st.button("⏮", disabled=current_page == 1):
                        st.session_state.page_num = 1
                        st.rerun()

                # Step backward one index
                with cols[1]:
                    if st.button("◀", disabled=current_page == 1):
                        st.session_state.page_num -= 1
                        st.rerun()

                # Text readout indicating current location sequence bounds
                with cols[2]:
                    st.markdown(
                        f"""
                        <div style="
                            text-align:center;
                            padding-top:8px; 
                            white-space:nowrap;
                            font-weight:600;
                        ">
                            Page {current_page} of {total_pages}
                        </div>
                    """,
                        unsafe_allow_html=True,
                    )

                # Step forward one index
                with cols[3]:
                    if st.button("▶", disabled=current_page == total_pages):
                        st.session_state.page_num += 1
                        st.rerun()

                # Navigate instantly to the absolute final available calculation range boundary
                with cols[4]:
                    if st.button("⏭", disabled=current_page == total_pages):
                        st.session_state.page_num = total_pages
                        st.rerun()

        except Exception as e:
            st.error(f"Error loading records: {e}")

        finally:
            # Always cleanly disconnect resources to free pool pipelines
            db.disconnect()
