-- ================================================================
-- CREDIT SYSTEM DATABASE SCHEMA
-- Comprehensive schema for credit risk assessment and loan management
-- ================================================================

CREATE DATABASE IF NOT EXISTS credit_system;
USE credit_system;

-- ================================================================
-- 1. USERS TABLE - Core user information
-- ================================================================
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    n_id VARCHAR(20) UNIQUE,
    user_type ENUM('new', 'old'),

    -- PERSONAL INFORMATION
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    
    age INT,
    gender ENUM('Male', 'Female'),
    marital_status VARCHAR(255),
    dependents INT,

    -- EMPLOYMENT INFORMATION
    education_level VARCHAR(255),
    employment_type VARCHAR(255),
    employment_tenure VARCHAR(255),
    work_experience VARCHAR(255),
    industry_type VARCHAR(255),
    position VARCHAR(255),

    -- RESIDENCE INFORMATION
    residence_type VARCHAR(255),
    living_duration VARCHAR(255),

    -- GEOGRAPHICAL INFORMATION
    geo_province VARCHAR(255),
    geo_district VARCHAR(255),
    geo_commune VARCHAR(255),
    geo_village VARCHAR(255),
    geo_is_urban BOOLEAN,

    -- RELATIONSHIP WITH PLATFORM
    relationship_with_platform VARCHAR(255),
    
    -- LOAN HISTORY
    loan_cycle_count INT DEFAULT 1,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- INDEXES
    INDEX idx_user_type (user_type),
    INDEX idx_province (geo_province),
    INDEX idx_employment_type (employment_type),
    INDEX idx_loan_cycle (loan_cycle_count)
);

-- ================================================================
-- 2. FINANCIAL_PROFILE TABLE - User financial information
-- ================================================================
CREATE TABLE IF NOT EXISTS financial_profile (
    financial_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,

    -- INCOME INFORMATION
    monthly_income DECIMAL(12,2),
    income_source_diversity INT,
    monthly_outflow DECIMAL(12,2),
    expense_ratio DECIMAL(6,4),
    net_cash_flow DECIMAL(12,2),
    monthly_debt_payment DECIMAL(12,2),
	surplus_income DECIMAL(12,2),

    -- FINANCIAL RESILIENCE
    saving_indicator BOOLEAN,
    guarantee_support BOOLEAN,
    asset_ownership VARCHAR(255),

    -- FINANCIAL TRENDS
    income_stability_trend VARCHAR(255),
    spending_trend VARCHAR(255),
    saving_trend VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_income (monthly_income)
);

-- ================================================================
-- 3. LOAN_INFORMATION TABLE - Current and historical loan details
-- ================================================================
CREATE TABLE IF NOT EXISTS loan_information (
    loan_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,

    -- LOAN DETAILS
    loan_amount DECIMAL(12,2),
    loan_tenure INT,
    loan_purpose VARCHAR(255),

    -- DEBT INFORMATION
    existing_loan_count INT,
    total_debt_amount DECIMAL(12,2),

    -- FINANCIAL RATIOS
    dti_ratio DECIMAL(5,2),
    lti_ratio DECIMAL(5,2),
    affordability_ratio DECIMAL(5,2),

    -- APPLICATION BEHAVIOR
    application_frequency VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_loan_amount (loan_amount),
    INDEX idx_dti_ratio (dti_ratio)
);

-- ================================================================
-- 4. IDENTITY_VERIFICATION TABLE - Identity and fraud verification
-- ================================================================
CREATE TABLE IF NOT EXISTS identity_verification (
    verification_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,

    -- VERIFICATION STATUS
    id_verification_status VARCHAR(255),
    phone_number_age VARCHAR(255),
    employment_application VARCHAR(255),
    social_media_link_account VARCHAR(255),
    nid_check VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_verification_status (id_verification_status)
);

-- ================================================================
-- 5. REPAYMENT_BEHAVIOR TABLE - Payment history and behavior
-- ================================================================
CREATE TABLE IF NOT EXISTS repayment_behavior (
    repayment_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,

    -- PAYMENT BEHAVIOR
    on_time_payment_rate DECIMAL(5,2),
    max_dpd INT,
    early_repayment_count INT,
    good_borrower_streak INT,
    partial_payment VARCHAR(255),
    loan_cycle_count INT,
    reborrow_frequency VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_payment_rate (on_time_payment_rate),
    INDEX idx_max_dpd (max_dpd)
);

-- ================================================================
-- 6. CREDIT_SCORING TABLE - Detailed credit scoring components
-- ================================================================
CREATE TABLE IF NOT EXISTS credit_scoring (
    score_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,

    -- SCORING COMPONENTS
    repayment_capacity_score DECIMAL(5,2),
    debt_exposure_score DECIMAL(5,2),
    stability_score DECIMAL(5,2),
    fraud_score DECIMAL(5,2),
    behavior_score DECIMAL(5,2),
    resilience_score DECIMAL(5,2),

    -- OVERALL SCORE
    final_credit_score DECIMAL(5,2),
    risk_level VARCHAR(255),
    approval_status VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_final_score (final_credit_score),
    INDEX idx_risk_level (risk_level),
    INDEX idx_approval_status (approval_status)
);

-- ================================================================
-- 7. PREDICTION_RESULT TABLE - Default prediction results
-- ================================================================
CREATE TABLE IF NOT EXISTS prediction_result (
    prediction_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,

    -- PREDICTION
    default_probability DECIMAL(5,2),
    prediction_label VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_prediction_label (prediction_label),
    INDEX idx_default_probability (default_probability),
    INDEX idx_created_at (created_at)
);

CREATE INDEX idx_user_full_name ON users (first_name, last_name);
CREATE INDEX idx_financial_profile_income_outflow ON financial_profile (monthly_income, monthly_outflow);
CREATE INDEX idx_loan_dti_lti ON loan_information (dti_ratio, lti_ratio);
CREATE INDEX idx_credit_scoring_composite ON credit_scoring (risk_level, approval_status, final_credit_score);
CREATE INDEX idx_prediction_probability_label ON prediction_result (default_probability, prediction_label);

CREATE TABLE IF NOT EXISTS assessment_history (
    assessment_id INT PRIMARY KEY AUTO_INCREMENT,

    user_id INT NOT NULL,

    assessment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    model_used VARCHAR(50),

    final_credit_score DECIMAL(6,2),

    default_probability DECIMAL(6,2),

    risk_level VARCHAR(50),

    recommendation VARCHAR(50),

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    INDEX idx_user_id(user_id),
    INDEX idx_assessment_date(assessment_date)
);

CREATE VIEW vw_credit_dashboard AS
SELECT
    u.user_id,
    u.n_id,
    CONCAT(u.first_name,' ',u.last_name) AS full_name,
    u.user_type,
    u.gender,
    u.age,

    fp.monthly_income,
    fp.monthly_outflow,
    fp.net_cash_flow,

    li.loan_amount,
    li.loan_tenure,
    li.dti_ratio,
    li.lti_ratio,

    cs.final_credit_score,
    cs.risk_level,
    cs.approval_status,

    pr.default_probability,
    pr.prediction_label

FROM users u
LEFT JOIN financial_profile fp
    ON u.user_id = fp.user_id
LEFT JOIN loan_information li
    ON u.user_id = li.user_id
LEFT JOIN credit_scoring cs
    ON u.user_id = cs.user_id
LEFT JOIN prediction_result pr
    ON u.user_id = pr.user_id;
    
DELIMITER $$

CREATE PROCEDURE sp_search_customer(
    IN p_nid VARCHAR(20)
)
BEGIN

    SELECT *
    FROM vw_credit_dashboard
    WHERE n_id = p_nid;

END $$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE sp_dashboard_statistics()
BEGIN

    SELECT
        COUNT(*) AS total_users
    FROM users;

    SELECT
        COUNT(*) AS approved_applications
    FROM credit_scoring
    WHERE approval_status='Approved';

    SELECT
        COUNT(*) AS rejected_applications
    FROM credit_scoring
    WHERE approval_status='Rejected';

    SELECT
        AVG(final_credit_score) AS average_credit_score
    FROM credit_scoring;

END $$

DELIMITER ;


DELIMITER $$

CREATE PROCEDURE sp_high_risk_customers()
BEGIN

    SELECT
        u.user_id,
        u.n_id,
        CONCAT(u.first_name,' ',u.last_name) AS full_name,
        cs.final_credit_score,
        cs.risk_level,
        pr.default_probability

    FROM users u

    JOIN credit_scoring cs
        ON u.user_id = cs.user_id

    JOIN prediction_result pr
        ON u.user_id = pr.user_id

    WHERE
        cs.risk_level='High'
        OR pr.default_probability >= 70

    ORDER BY pr.default_probability DESC;

END $$

DELIMITER ;


DELIMITER $$

CREATE PROCEDURE sp_customer_credit_profile(
    IN p_nid VARCHAR(20)
)
BEGIN

    SELECT
        u.*,
        fp.*,
        li.*,
        iv.*,
        rb.*,
        cs.*,
        pr.*

    FROM users u

    LEFT JOIN financial_profile fp
        ON u.user_id = fp.user_id

    LEFT JOIN loan_information li
        ON u.user_id = li.user_id

    LEFT JOIN identity_verification iv
        ON u.user_id = iv.user_id

    LEFT JOIN repayment_behavior rb
        ON u.user_id = rb.user_id

    LEFT JOIN credit_scoring cs
        ON u.user_id = cs.user_id

    LEFT JOIN prediction_result pr
        ON u.user_id = pr.user_id

    WHERE u.n_id = p_nid;

END $$

DELIMITER ;

CREATE INDEX idx_nid
ON users(n_id);

CREATE INDEX idx_created_user
ON users(created_at);

CREATE INDEX idx_score
ON credit_scoring(final_credit_score);

CREATE INDEX idx_default_prob
ON prediction_result(default_probability);

