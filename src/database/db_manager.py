import logging
from typing import Dict, Optional

import mysql.connector
from mysql.connector import Error
from sqlalchemy import values

from src.config.settings import DB_CONFIG

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class DemoDBManager:
    """Database helper for saving credit assessment results."""

    def __init__(self, config: Dict = DB_CONFIG):
        self.config = config
        self.connection = None
        self.cursor = None

    def connect(self) -> bool:
        try:
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor()
            logger.info("Connected to credit_system database")
            return True
        except Error as e:
            logger.error(f"Database connection error: {e}")
            return False

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Database connection closed")

    def _execute(self, query: str, params: tuple = ()) -> Optional[int]:
        try:
            self.cursor.execute(query, params)
            return self.cursor.lastrowid
        except Error as e:
            logger.error(f"SQL execution error: {e}")
            raise

    def create_user(self, user_data: Dict) -> int:
        query = """
            INSERT INTO users (
                n_id, user_type, first_name, last_name, age, gender,
                marital_status, dependents, education_level, employment_type,
                employment_tenure, work_experience, industry_type, position,
                residence_type, living_duration, geo_province, geo_district,
                geo_commune, geo_village, geo_is_urban, relationship_with_platform,
                loan_cycle_count
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            user_data.get("n_id"),
            user_data.get("user_type"),
            user_data.get("first_name"),
            user_data.get("last_name"),
            user_data.get("age"),
            user_data.get("gender"),
            user_data.get("marital_status"),
            user_data.get("dependents"),
            user_data.get("education_level"),
            user_data.get("employment_type"),
            user_data.get("employment_tenure"),
            user_data.get("work_experience"),
            user_data.get("industry_type"),
            user_data.get("position"),
            user_data.get("residence_type"),
            user_data.get("living_duration"),
            user_data.get("geo_province"),
            user_data.get("geo_district"),
            user_data.get("geo_commune"),
            user_data.get("geo_village"),
            user_data.get("geo_is_urban"),
            user_data.get("relationship_with_platform"),
            user_data.get("loan_cycle_count"),
        )
        return self._execute(query, values)

    def get_user_by_nid(self, n_id: str) -> Optional[Dict]:
        query = "SELECT * FROM users WHERE n_id = %s LIMIT 1"
        self.cursor.execute(query, (n_id,))
        row = self.cursor.fetchone()
        if not row:
            return None
        return dict(zip(self.cursor.column_names, row))

    def record_exists(self, table: str, user_id: int) -> bool:
        query = f"SELECT 1 FROM {table} WHERE user_id = %s LIMIT 1"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone() is not None

    def update_user(self, user_id: int, user_data: Dict) -> int:
        query = """
            UPDATE users SET
                user_type = %s,
                first_name = %s,
                last_name = %s,
                age = %s,
                gender = %s,
                marital_status = %s,
                dependents = %s,
                education_level = %s,
                employment_type = %s,
                employment_tenure = %s,
                work_experience = %s,
                industry_type = %s,
                position = %s,
                residence_type = %s,
                living_duration = %s,
                geo_province = %s,
                geo_district = %s,
                geo_commune = %s,
                geo_village = %s,
                geo_is_urban = %s,
                relationship_with_platform = %s,
                loan_cycle_count = %s
            WHERE user_id = %s
        """
        values = (
            user_data.get("user_type"),
            user_data.get("first_name"),
            user_data.get("last_name"),
            user_data.get("age"),
            user_data.get("gender"),
            user_data.get("marital_status"),
            user_data.get("dependents"),
            user_data.get("education_level"),
            user_data.get("employment_type"),
            user_data.get("employment_tenure"),
            user_data.get("work_experience"),
            user_data.get("industry_type"),
            user_data.get("position"),
            user_data.get("residence_type"),
            user_data.get("living_duration"),
            user_data.get("geo_province"),
            user_data.get("geo_district"),
            user_data.get("geo_commune"),
            user_data.get("geo_village"),
            user_data.get("geo_is_urban"),
            user_data.get("relationship_with_platform"),
            user_data.get("loan_cycle_count"),
            user_id,
        )
        self.cursor.execute(query, values)
        return user_id

    def update_or_insert_financial_profile(
        self, user_id: int, financial_data: Dict
    ) -> int:
        if self.record_exists("financial_profile", user_id):
            query = """
                UPDATE financial_profile SET
                    monthly_income = %s,
                    income_source_diversity = %s,
                    monthly_outflow = %s,
                    expense_ratio = %s,
                    net_cash_flow = %s,
                    monthly_debt_payment = %s,
                    surplus_income = %s,
                    saving_indicator = %s,
                    guarantee_support = %s,
                    asset_ownership = %s,
                    income_stability_trend = %s,
                    spending_trend = %s,
                    saving_trend = %s
                WHERE user_id = %s
            """
            values = (
                financial_data.get("monthly_income"),
                financial_data.get("income_source_diversity"),
                financial_data.get("monthly_outflow"),
                financial_data.get("expense_ratio"),
                financial_data.get("net_cash_flow"),
                financial_data.get("monthly_debt_payment"),
                financial_data.get("surplus_income"),
                financial_data.get("saving_indicator"),
                financial_data.get("guarantee_support"),
                financial_data.get("asset_ownership"),
                financial_data.get("income_stability_trend"),
                financial_data.get("spending_trend"),
                financial_data.get("saving_trend"),
                user_id,
            )
            self.cursor.execute(query, values)
            return user_id
        return self.add_financial_profile(user_id, financial_data)

    def update_or_insert_loan_information(self, user_id: int, loan_data: Dict) -> int:
        if self.record_exists("loan_information", user_id):
            query = """
                UPDATE loan_information SET
                    loan_amount = %s,
                    loan_tenure = %s,
                    loan_purpose = %s,
                    existing_loan_count = %s,
                    total_debt_amount = %s,
                    dti_ratio = %s,
                    lti_ratio = %s,
                    affordability_ratio = %s,
                    application_frequency = %s
                WHERE user_id = %s
            """
            values = (
                loan_data.get("loan_amount"),
                loan_data.get("loan_tenure"),
                loan_data.get("loan_purpose"),
                loan_data.get("existing_loan_count"),
                loan_data.get("total_debt_amount"),
                loan_data.get("dti_ratio"),
                loan_data.get("lti_ratio"),
                loan_data.get("affordability_ratio"),
                loan_data.get("application_frequency"),
                user_id,
            )
            self.cursor.execute(query, values)
            return user_id
        return self.add_loan_information(user_id, loan_data)

    def update_or_insert_identity_verification(
        self, user_id: int, identity_data: Dict
    ) -> int:
        if self.record_exists("identity_verification", user_id):
            query = """
                UPDATE identity_verification SET
                    id_verification_status = %s,
                    phone_number_age = %s,
                    employment_application = %s,
                    social_media_link_account = %s,
                    nid_check = %s
                WHERE user_id = %s
            """
            values = (
                identity_data.get("id_verification_status"),
                identity_data.get("phone_number_age"),
                identity_data.get("employment_application"),
                identity_data.get("social_media_link_account"),
                identity_data.get("nid_check"),
                user_id,
            )
            self.cursor.execute(query, values)
            return user_id
        return self.add_identity_verification(user_id, identity_data)

    def update_or_insert_credit_scoring(self, user_id: int, score_data: Dict) -> int:
        if self.record_exists("credit_scoring", user_id):
            query = """
                UPDATE credit_scoring SET
                    repayment_capacity_score = %s,
                    debt_exposure_score = %s,
                    stability_score = %s,
                    fraud_score = %s,
                    behavior_score = %s,
                    resilience_score = %s,
                    final_credit_score = %s,
                    risk_level = %s,
                    approval_status = %s
                WHERE user_id = %s
            """
            values = (
                score_data.get("repayment_capacity_score"),
                score_data.get("debt_exposure_score"),
                score_data.get("stability_score"),
                score_data.get("fraud_score"),
                score_data.get("behavior_score"),
                score_data.get("resilience_score"),
                score_data.get("final_credit_score"),
                score_data.get("risk_level"),
                score_data.get("approval_status"),
                user_id,
            )
            self.cursor.execute(query, values)
            return user_id
        return self.add_credit_scoring(user_id, score_data)

    def update_or_insert_prediction_result(
        self, user_id: int, prediction_data: Dict
    ) -> int:
        if self.record_exists("prediction_result", user_id):
            query = """
                UPDATE prediction_result SET
                    default_probability = %s,
                    prediction_label = %s
                WHERE user_id = %s
            """
            values = (
                prediction_data.get("default_probability"),
                prediction_data.get("prediction_label"),
                user_id,
            )
            self.cursor.execute(query, values)
            return user_id
        return self.add_prediction_result(user_id, prediction_data)

    def update_or_insert_repayment_behavior(
        self, user_id: int, repayment_data: Dict
    ) -> int:
        if self.record_exists("repayment_behavior", user_id):
            query = """
                UPDATE repayment_behavior SET
                    on_time_payment_rate = %s,
                    max_dpd = %s,
                    early_repayment_count = %s,
                    good_borrower_streak = %s,
                    partial_payment = %s,
                    loan_cycle_count = %s,
                    reborrow_frequency = %s
                WHERE user_id = %s
            """
            values = (
                repayment_data.get("on_time_payment_rate"),
                repayment_data.get("max_dpd"),
                repayment_data.get("early_repayment_count"),
                repayment_data.get("good_borrower_streak"),
                repayment_data.get("partial_payment"),
                repayment_data.get("loan_cycle_count"),
                repayment_data.get("reborrow_frequency"),
                user_id,
            )
            self.cursor.execute(query, values)
            return user_id
        return self.add_repayment_behavior(user_id, repayment_data)

    def save_assessment(
        self,
        user_data: Dict,
        financial_data: Dict,
        loan_data: Dict,
        identity_data: Dict,
        score_data: Dict,
        prediction_data: Dict,
        repayment_data: Optional[Dict] = None,
        existing_user_id: Optional[int] = None,
    ) -> bool:
        try:
            self.connection.start_transaction()
            if existing_user_id:
                user_id = existing_user_id
                # Preserve the original user record for ML/history and insert a new assessment row for the old-user session.
            else:
                user_id = self.create_user(user_data)
                if not user_id:
                    raise Error("Failed to insert user")

            if existing_user_id:
                self.add_financial_profile(user_id, financial_data)
                self.add_loan_information(user_id, loan_data)
                self.add_identity_verification(user_id, identity_data)
                self.add_credit_scoring(user_id, score_data)
                self.add_prediction_result(user_id, prediction_data)
                if repayment_data is not None:
                    self.add_repayment_behavior(user_id, repayment_data)
            else:
                self.update_or_insert_financial_profile(user_id, financial_data)
                self.update_or_insert_loan_information(user_id, loan_data)
                self.update_or_insert_identity_verification(user_id, identity_data)
                self.update_or_insert_credit_scoring(user_id, score_data)
                self.update_or_insert_prediction_result(user_id, prediction_data)
                if repayment_data is not None:
                    self.update_or_insert_repayment_behavior(user_id, repayment_data)

            self.connection.commit()
            logger.info(f"Saved assessment records for user {user_id}")
            return True

        except Error as e:
            logger.error(f"Failed to save assessment: {e}")
            print(f"MYSQL ERROR: {e}")

            if self.connection:
                self.connection.rollback()
            raise

    def add_financial_profile(self, user_id: int, financial_data: Dict) -> int:
        query = """
            INSERT INTO financial_profile (
                user_id, monthly_income, income_source_diversity,
                monthly_outflow, expense_ratio, net_cash_flow,
                saving_indicator, guarantee_support, asset_ownership,
                income_stability_trend, spending_trend, saving_trend
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            user_id,
            financial_data.get("monthly_income"),
            financial_data.get("income_source_diversity"),
            financial_data.get("monthly_outflow"),
            financial_data.get("expense_ratio"),
            financial_data.get("net_cash_flow"),
            financial_data.get("saving_indicator"),
            financial_data.get("guarantee_support"),
            financial_data.get("asset_ownership"),
            financial_data.get("income_stability_trend"),
            financial_data.get("spending_trend"),
            financial_data.get("saving_trend"),
        )
        return self._execute(query, values)

    def add_loan_information(self, user_id: int, loan_data: Dict) -> int:
        query = """
            INSERT INTO loan_information (
                user_id, loan_amount, loan_tenure, loan_purpose,
                existing_loan_count, total_debt_amount, dti_ratio,
                lti_ratio, affordability_ratio, application_frequency
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            user_id,
            loan_data.get("loan_amount"),
            loan_data.get("loan_tenure"),
            loan_data.get("loan_purpose"),
            loan_data.get("existing_loan_count"),
            loan_data.get("total_debt_amount"),
            loan_data.get("dti_ratio"),
            loan_data.get("lti_ratio"),
            loan_data.get("affordability_ratio"),
            loan_data.get("application_frequency"),
        )
        return self._execute(query, values)

    def add_identity_verification(self, user_id: int, identity_data: Dict) -> int:
        query = """
            INSERT INTO identity_verification (
                user_id, id_verification_status, phone_number_age,
                employment_application, social_media_link_account, nid_check
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            user_id,
            identity_data.get("id_verification_status"),
            identity_data.get("phone_number_age"),
            identity_data.get("employment_application"),
            identity_data.get("social_media_link_account"),
            identity_data.get("nid_check"),
        )
        return self._execute(query, values)

    def add_repayment_behavior(self, user_id: int, repayment_data: Dict) -> int:
        query = """
            INSERT INTO repayment_behavior (
                user_id, on_time_payment_rate, max_dpd,
                early_repayment_count, good_borrower_streak,
                partial_payment, loan_cycle_count, reborrow_frequency
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            user_id,
            repayment_data.get("on_time_payment_rate"),
            repayment_data.get("max_dpd"),
            repayment_data.get("early_repayment_count"),
            repayment_data.get("good_borrower_streak"),
            repayment_data.get("partial_payment"),
            repayment_data.get("loan_cycle_count"),
            repayment_data.get("reborrow_frequency"),
        )
        return self._execute(query, values)

    def add_credit_scoring(self, user_id: int, score_data: Dict) -> int:
        query = """
            INSERT INTO credit_scoring (
                user_id, repayment_capacity_score, debt_exposure_score,
                stability_score, fraud_score, behavior_score,
                resilience_score, final_credit_score, risk_level,
                approval_status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            user_id,
            score_data.get("repayment_capacity_score"),
            score_data.get("debt_exposure_score"),
            score_data.get("stability_score"),
            score_data.get("fraud_score"),
            score_data.get("behavior_score"),
            score_data.get("resilience_score"),
            score_data.get("final_credit_score"),
            score_data.get("risk_level"),
            score_data.get("approval_status"),
        )
        return self._execute(query, values)

    def add_prediction_result(self, user_id: int, prediction_data: Dict) -> int:
        query = """
            INSERT INTO prediction_result (
                user_id, default_probability, prediction_label
            ) VALUES (%s, %s, %s)
        """
        values = (
            user_id,
            prediction_data.get("default_probability"),
            prediction_data.get("prediction_label"),
        )
        return self._execute(query, values)

    def add_assessment_history(
        self,
        user_id: int,
        model_used: str,
        score: float,
        probability: float,
        risk_level: str,
        recommendation: str,
    ):
        query = """
            INSERT INTO assessment_history (
                user_id,
                model_used,
                final_credit_score,
                default_probability,
                risk_level,
                recommendation
            )
            VALUES (%s,%s,%s,%s,%s,%s)
        """

        values = (user_id, model_used, score, probability, risk_level, recommendation)
        return self._execute(query, values)
