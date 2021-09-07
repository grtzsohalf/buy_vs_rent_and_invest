#! /usr/bin/bash

yearly_interest_rate_list='0.014 0.015 0.016 0.017 0.018'
loan_term_list='20.0 25.0 30.0 35.0 40.0'
house_price=10000000.0
loan_proportion=0.7
price_after_loan_term=12000000.0
payment_method='equal_total_payment'
rent_per_month=30000.0

python3 buy_vs_rent_and_invest.py \
  --yearly_interest_rate_list $yearly_interest_rate_list \
  --loan_term_list $loan_term_list \
  --house_price $house_price \
  --loan_proportion $loan_proportion \
  --price_after_loan_term $price_after_loan_term \
  --payment_method $payment_method \
  --rent_per_month $rent_per_month
