#!/usr/bin/env python

## Copyright 2014 Francesco Bailo

## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.

# parseKivaDump.py

# Call it from console passing database filename: python parseKivaDump.py <dump folder> <database>

import sqlite3
import sys
import os
import json

# Receive the arguments from bash
dump_dir = sys.argv[1]
database = sys.argv[2] + '.sqlite'

## Functions

def main (dump_dir, database):

    lenders_dir = dump_dir + "/lenders/"
    loans_dir = dump_dir + "/loans/"
    loans_lenders_dir = dump_dir + "/loans_lenders/"

    parseLenders(lenders_dir, database)
    parseLoans(loans_dir, database)
    parseLoansLenders(loans_lenders_dir, database)

def parseJsonFile (json_file):
    
    json_data = open(json_file)
    data = json.load(json_data)
    json_data.close()
    return data

def parseLenders (lenders_dir, database):

    # Loop through all files
    for file in os.listdir(lenders_dir):
        print file
        if file.endswith(".json"):

            data = parseJsonFile(lenders_dir + file)

            counter = 0

            # Open db connection
            conn = sqlite3.connect(database)
            cursor = conn.cursor()

            for lender_item in data['lenders']:

                print counter

                # Parse lender
                lender = {}
                lender['lender_id'] = lender_item.get('lender_id')
                lender['country_code'] = lender_item.get('country_code')
                lender['invitee_count'] = lender_item.get('invitee_count')
                lender['inviter_id'] = lender_item.get('inviter_id')
                lender['loan_because'] = lender_item.get('loan_because')
                lender['loan_count'] = lender_item.get('loan_count')
                lender['member_since'] = lender_item.get('member_since')
                lender['name'] = lender_item.get('name')
                lender['occupation'] = lender_item.get('occupation')
                lender['occupational_info'] = lender_item.get('occupational_info')
                lender['personal_url'] = lender_item.get('personal_url')
                lender['uid'] = lender_item.get('uid')
                lender['whereabouts'] = lender_item.get('whereabouts')

                # Enter lender into database
                enterLender(lender, cursor)

                counter += 1

            conn.commit()

    return


def parseLoans (loans_dir, database):

    # Loop through all files
    for file in os.listdir(loans_dir):
        print file
        if file.endswith(".json"):

            data = parseJsonFile(loans_dir + file)

            counter = 0

            # Open db connection
            conn = sqlite3.connect(database)
            cursor = conn.cursor()

            for loan_item in data['loans']:

                print counter

                # Parse loan
                loan = {}
                loan['loan_id'] = loan_item.get('id')
                loan['activity'] = loan_item.get('activity')
                loan['basket_amount'] = loan_item.get('basket_amount')
                loan['bonus_credit_eligibility'] = loan_item.get('bonus_credit_eligibility')
                loan['currency_exchange_loss_amount'] = loan_item.get('currency_exchange_loss_amount')
                loan['delinquent'] = loan_item.get('delinquent')
                loan['description'] = loan_item['description']['texts'].get('en')
                loan['funded_amount'] = loan_item.get('funded_amount')
                loan['funded_date'] = loan_item.get('funded_date')
                loan['journal_totals'] = loan_item['journal_totals'].get('entries')
                loan['lender_count'] = loan_item.get('lender_count')
                loan['loan_amount'] = loan_item.get('loan_amount')
                loan['name'] = loan_item.get('name')
                loan['paid_amount'] = loan_item.get('paid_amount')
                loan['paid_date'] = loan_item.get('paid_date')
                loan['partner_id'] = loan_item.get('partner_id')
                loan['planned_expiration_date'] = loan_item.get('planned_expiration_date')
                loan['posted_date'] = loan_item.get('posted_date')
                loan['sector'] = loan_item.get('sector')
                loan['status'] = loan_item.get('status')
                loan['theme'] = loan_item.get('theme')
                loan['translator'] = loan_item.get('translator')
                if isinstance(loan['translator'], dict):
                    loan['translator'] = loan['translator'].get('byline')
                loan['use'] = loan_item.get('use')

                # Enter loan into database
                enterLoan(loan, cursor)

                # Parse borrowers
                for borrower_item in loan_item['borrowers']:
                    borrower = {}
                    borrower['loan_id'] = loan['loan_id']
                    borrower['first_name'] = borrower_item.get('first_name')
                    borrower['gender'] = borrower_item.get('gender')
                    borrower['last_name'] = borrower_item.get('last_name')

                    # Enter borrower into database
                    enterBorrower(borrower, cursor)

                # Parse location    
                location = {}
                location['loan_id'] = loan['loan_id']
                location['country'] = loan_item['location'].get('country')
                location['country_code'] = loan_item['location'].get('country_code')
                location['geo_level'] = loan_item['location'].get('geo').get('level')
                location['geo_pairs'] = loan_item['location'].get('geo').get('pairs')
                location['geo_type'] = loan_item['location'].get('geo').get('type')
                location['town'] = loan_item['location'].get('town')

                # Enter location into database
                enterLocation(location, cursor)

                # Parse payments
                for payment_item in loan_item['payments']:
                    payment = {}
                    payment['loan_id'] = loan['loan_id']
                    payment['amount'] = payment_item.get('amount')
                    payment['comment'] = payment_item.get('comment')
                    payment['currency_exchange_loss_amount'] = payment_item.get('currency_exchange_loss_amount')
                    payment['local_amount'] = payment_item.get('local_amount')
                    payment['payment_id'] = payment_item.get('payment_id')
                    payment['processed_date'] = payment_item.get('processed_date')
                    payment['rounded_local_amount'] = payment_item.get('rounded_local_amount')
                    payment['settlement_date'] = payment_item.get('settlement_date')

                    # Enter payment into database
                    enterPayment(payment, cursor)

                # Parse terms    
                terms = {}
                terms['loan_id'] = loan['loan_id']
                terms['disbursal_amount'] = loan_item['terms'].get('disbursal_amount')
                terms['disbursal_currency'] = loan_item['terms'].get('disbursal_currency')
                terms['disbursal_date'] = loan_item['terms'].get('disbursal_date')
                terms['loan_amount'] = loan_item['terms'].get('loan_amount')
                terms['loss_liability_currency_exchange'] = loan_item['terms'].get('loss_liability').get('currency_exchange')
                terms['loss_liability_currency_exchange_coverage_rate'] = loan_item['terms'].get('loss_liability').get('currency_exchange_coverage_rate')
                terms['loss_liability_nonpayment'] = loan_item['terms'].get('loss_liability').get('nonpayment')
                terms['repayment_interval'] = loan_item['terms'].get('repayment_interval')
                terms['repayment_term'] = loan_item['terms'].get('repayment_term')

                # Enter terms into database
                enterTerms(terms, cursor)

                # Parse local payment
                for local_payment_item in loan_item['terms'].get('local_payments'):
                    local_payment = {}
                    local_payment['loan_id'] = loan['loan_id']
                    local_payment['amount'] = local_payment_item.get('amount')
                    local_payment['due_date'] = local_payment_item.get('due_date')

                    # Enter local payment into database
                    enterLocalPayment(local_payment, cursor)

                # Parse scheduled payment
                for scheduled_payment_item in loan_item['terms'].get('scheduled_payments'):
                    scheduled_payment = {}
                    scheduled_payment['loan_id'] = loan['loan_id']
                    scheduled_payment['amount'] = scheduled_payment_item.get('amount')
                    scheduled_payment['due_date'] = scheduled_payment_item.get('due_date')

                    # Enter scheduled payment into database
                    enterScheduledPayment(scheduled_payment, cursor)
                    
                conn.commit()

                counter += 1

    return
            

def parseLoansLenders (loans_lenders_dir, database):

    # Loop through all files
    for file in os.listdir(loans_lenders_dir):
        print file
        if file.endswith(".json"):

            data = parseJsonFile(loans_lenders_dir + file)

            counter = 0

            # Open db connection
            conn = sqlite3.connect(database)
            cursor = conn.cursor()

            for loan_lender_item in data['loans_lenders']:

                print counter

                # Parse loan lender
                loan_id = loan_lender_item.get('id')
                if isinstance(loan_lender_item['lender_ids'], list):
                    for lender_item in loan_lender_item['lender_ids']:
                        loan_lender = {}
                        loan_lender['loan_id'] = loan_id
                        loan_lender['lender_id'] = lender_item

                        # Enter lender into database
                        enterLoanLender(loan_lender, cursor)
                else:
                    loan_lender = {}
                    loan_lender['loan_id'] = loan_id
                    loan_lender['lender_id'] = None
                    
                    # Enter lender into database
                    enterLoanLender(loan_lender, cursor)
                    
                counter += 1

            conn.commit()

    return


def enterLoan (object, cursor):

    cursor.execute("INSERT OR IGNORE INTO loan (loan_id, activity, basket_amount, bonus_credit_eligibility, currency_exchange_loss_amount, delinquent, description, funded_amount, funded_date, journal_totals, lender_count, loan_amount, name, paid_amount, paid_date, partner_id, planned_expiration_date, posted_date, sector, status, theme, translator, use) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (object['loan_id'], object['activity'], object['basket_amount'], object['bonus_credit_eligibility'], object['currency_exchange_loss_amount'], object['delinquent'], object['description'], object['funded_amount'], object['funded_date'], object['journal_totals'], object['lender_count'], object['loan_amount'], object['name'], object['paid_amount'], object['paid_date'], object['partner_id'], object['planned_expiration_date'], object['posted_date'], object['sector'], object['status'], object['theme'], object['translator'], object['use']))    

    return


def enterBorrower (object, cursor):

    cursor.execute("INSERT OR IGNORE INTO borrower (loan_id, first_name, gender, last_name) VALUES (?, ?, ?, ?)", (object['loan_id'],object['first_name'],object['gender'],object['last_name']))

    return

    
def enterLocation (object, cursor):

    cursor.execute("INSERT OR IGNORE INTO location (loan_id, country, country_code, geo_level, geo_pairs, geo_type, town) VALUES (?, ?, ?, ?, ?, ?, ?)", (object['loan_id'], object['country'], object['country_code'], object['geo_level'], object['geo_pairs'], object['geo_type'], object['town']))

    return


def enterPayment (object, cursor):

    cursor.execute("INSERT OR IGNORE INTO payment (payment_id, loan_id, amount, comment, currency_exchange_loss_amount, local_amount, processed_date, rounded_local_amount, settlement_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (object['payment_id'], object['loan_id'], object['amount'], object['comment'], object['currency_exchange_loss_amount'], object['local_amount'], object['processed_date'], object['rounded_local_amount'], object['settlement_date']))

    return
    

def enterTerms (object, cursor):

    cursor.execute("INSERT OR IGNORE INTO terms (loan_id, disbursal_amount, disbursal_currency, disbursal_date, loan_amount, loss_liability_currency_exchange, loss_liability_currency_exchange_coverage_rate, loss_liability_nonpayment, repayment_interval, repayment_term) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (object['loan_id'], object['disbursal_amount'], object['disbursal_currency'], object['disbursal_date'], object['loan_amount'], object['loss_liability_currency_exchange'], object['loss_liability_currency_exchange_coverage_rate'], object['loss_liability_nonpayment'], object['repayment_interval'], object['repayment_term']))

    return


def enterLender (object, cursor):

    cursor.execute("INSERT OR IGNORE INTO lender (lender_id, country_code, invitee_count, inviter_id, loan_because, loan_count, member_since, name, occupation, occupational_info, personal_url, uid, whereabouts) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (object['lender_id'], object['country_code'], object['invitee_count'], object['inviter_id'], object['loan_because'], object['loan_count'], object['member_since'], object['name'], object['occupation'], object['occupational_info'], object['personal_url'], object['uid'], object['whereabouts']))

    return


def enterLoanLender (object, cursor):

    cursor.execute("INSERT OR IGNORE INTO loan_lender (loan_id, lender_id) VALUES (?, ?)", (object['loan_id'], object['lender_id']))

    return

def enterLocalPayment (object, cursor):

    cursor.execute("INSERT OR IGNORE INTO local_payment (loan_id, amount, due_date) VALUES (?, ?, ?)", (object['loan_id'], object['amount'],  object['due_date']))

    return

def enterScheduledPayment (object, cursor):

    cursor.execute("INSERT OR IGNORE INTO scheduled_payment (loan_id, amount, due_date) VALUES (?, ?, ?)", (object['loan_id'], object['amount'],  object['due_date']))

    return
    

# Execute the program
main(dump_dir, database)
