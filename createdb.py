#!/usr/bin/env python

# createdb.py

# Call it from console passing database filename: python createdb.py filename

import sqlite3
import sys

# Receive the argument from bash
filename = sys.argv[1] + '.sqlite'
 
conn = sqlite3.connect(filename)
 
cursor = conn.cursor()
 
# Create database

# Create tables
cursor.execute("""
CREATE TABLE loan ( 
    loan_id INTEGER PRIMARY KEY,
    activity CHAR,
    basket_amount INTEGER,
    bonus_credit_eligibility BOOLEAN,
    currency_exchange_loss_amount INTEGER,
    delinquent BOOLEAN,
    description TEXT,
    funded_amount INTEGER,
    funded_date DATETIME,
    journal_totals INTEGER,
    lender_count INTEGER,
    loan_amount DOUBLE,
    name CHAR,
    paid_amount DOUBLE,
    paid_date DATETIME,
    partner_id INTEGER,
    planned_expiration_date DATETIME,
    posted_date DATETIME,
    sector CHAR,
    status CHAR,
    theme CHAR,
    translator CHAR,
    use TEXT,
    timestamp DATETIME DEFAULT ( CURRENT_TIMESTAMP ) 
    );
               """)

cursor.execute("""
CREATE TABLE borrower (
    borrower_id INTEGER PRIMARY KEY AUTOINCREMENT,
    loan_id INTEGER NOT NULL,
    first_name CHAR,
    gender CHAR,
    last_name CHAR,
    timestamp DATETIME DEFAULT ( CURRENT_TIMESTAMP ),
    FOREIGN KEY(loan_id) REFERENCES loan(loan_id)
    );
               """)

cursor.execute("""
CREATE TABLE location ( 
    loan_id INTEGER PRIMARY KEY,
    country CHAR,
    country_code CHAR,
    geo_level CHAR,
    geo_pairs CHAR,
    geo_type CHAR,
    town CHAR,
    timestamp DATETIME DEFAULT ( CURRENT_TIMESTAMP ),
    FOREIGN KEY(loan_id) REFERENCES loan(loan_id)
    );
               """)

cursor.execute("""
CREATE TABLE payment (
    payment_id INTEGER PRIMARY KEY,
    loan_id INTEGER NOT NULL,
    amount DOUBLE,
    comment TEXT,
    currency_exchange_loss_amount DOUBLE,
    local_amount DOUBLE,
    processed_date DATETIME,
    rounded_local_amount DOUBLE,
    settlement_date DATETIME,
    timestamp DATETIME DEFAULT ( CURRENT_TIMESTAMP ),
    FOREIGN KEY(loan_id) REFERENCES loan(loan_id)
    );
               """)

cursor.execute("""
CREATE TABLE terms (
    loan_id INTEGER PRIMARY KEY,
    disbursal_amount DOUBLE,
    disbursal_currency CHAR,
    disbursal_date DATETIME,
    loan_amount DOUBLE,
    loss_liability_currency_exchange CHAR,
    loss_liability_currency_exchange_coverage_rate CHAR,
    loss_liability_nonpayment CHAR,
    repayment_interval CHAR,
    repayment_term INTEGER,
    timestamp DATETIME DEFAULT ( CURRENT_TIMESTAMP ),
    FOREIGN KEY(loan_id) REFERENCES loan(loan_id)
    );
               """)

cursor.execute("""
CREATE TABLE lender ( 
    lender_id CHAR PRIMARY KEY,
    country_code CHAR,
    invitee_count INTEGER,
    inviter_id INTEGER,
    loan_because TEXT,
    loan_count INTEGER,
    member_since DATETIME,
    name CHAR,
    occupation CHAR,
    occupational_info TEXT,
    personal_url CHAR,
    uid CHAR,
    whereabouts TEXT,
    timestamp DATETIME DEFAULT ( CURRENT_TIMESTAMP ) 
    );
               """)

cursor.execute("""
CREATE TABLE loan_lender (
    loan_lender_id INTEGER PRIMARY KEY AUTOINCREMENT,
    loan_id INTEGER  NOT NULL,
    lender_id CHAR,
    timestamp DATETIME DEFAULT ( CURRENT_TIMESTAMP ),
    FOREIGN KEY(loan_id) REFERENCES loan(loan_id),
    FOREIGN KEY(lender_id) REFERENCES lender(lender_id)
    );
               """)

cursor.execute("""
CREATE TABLE local_payment (
    local_payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    loan_id INTEGER  NOT NULL,
    amount DOUBLE,
    due_date DATETIME,
    FOREIGN KEY(loan_id) REFERENCES loan(loan_id)
    );
               """)

cursor.execute("""
CREATE TABLE scheduled_payment (
    scheduled_payments_id INTEGER PRIMARY KEY AUTOINCREMENT,
    loan_id INTEGER NOT NULL,
    amount DOUBLE,
    due_date DATETIME,
    FOREIGN KEY(loan_id) REFERENCES loan(loan_id)
    );
               """)

# Close connection
conn.commit()
