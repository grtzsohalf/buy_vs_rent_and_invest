#!/bin/bash

yearly_interest_rate_list='0.014 0.015 0.016 0.017 0.018'
loan_term_list='20.0 25.0 30.0 35.0 40.0' # unit: year
house_price=15000000.0
loan_proportion=0.75 # the proportion of house_price - down_payment
house_price_increase_rate_in_5y=0.1 # the increase rate of house price in 5 years
payment_method='equal_total_payment' # Options are: 'equal_total_payment', 'equal_principal_payment'
rent_per_month=15000.0
monthly_budget=60000.0

python3 buy_vs_rent_and_invest.py \
  --yearly_interest_rate_list $yearly_interest_rate_list \
  --loan_term_list $loan_term_list \
  --house_price $house_price \
  --loan_proportion $loan_proportion \
  --house_price_increase_rate_in_5y $house_price_increase_rate_in_5y \
  --payment_method $payment_method \
  --rent_per_month $rent_per_month \
  --monthly_budget $monthly_budget
