import argparse
import matplotlib.pyplot as plt
import numpy as np



def addParser():
    parser = argparse.ArgumentParser()

    # The scenario 'B_and_R' has not been supported, so we assume it's the scenario 'B' below
    '''
    ### 2 scenarios 
    # 1.       'B': Buy a house (NOT rent to others)
    # 2. 'B_and_R': Buy a house (rent to others) and rent another one 
    parser.add_argument('--scenario', type=str, default='B', choices=['B', 'B_and_R'])
    parser.add_argument('--rent_to_others_per_month', type=float, default=30000.0)
    '''

    ### Buy
    parser.add_argument('--yearly_interest_rate_list', type=float, nargs='+', 
                        default=[0.014, 0.015, 0.016, 0.017, 0.018], 
                        help='假設是固定利率非機動利率（但其實多為機動利率）')
    # 2021 青年首購安心成家購屋優惠方案，確定延後到 111 年 2022 年 12 月 31 日。
    # 須本息平均攤還，最高額度 800 萬、目前總費用年百分率1.4%，
    # 申辦時間為 110 年 1 月 1 日至 111 年 12 月 31 日。
    # 一般銀行一段式首購有機會利率更低。

    parser.add_argument('--loan_term_list', type=float, nargs='+', 
                        default=[20.0, 25.0, 30.0, 35.0, 40.0], 
                        help='unit: year')
    parser.add_argument('--house_price', type=float, default=10000000.0) 
    parser.add_argument('--loan_proportion', type=float, default=0.7)
    parser.add_argument('--price_after_loan_term', type=float, default=12000000.0)

    # Note: Suppose the loan is monthly paid
    parser.add_argument('--payment_method', type=str, default='equal_total_payment', 
                        choices=['equal_total_payment', 'equal_principal_payment'], 
                        help='equal_total_payment: 本息平均攤還, equal_principal_payment: 本金平均攤還')
    # Suppose 
    # (1) principal = A
    # (2) interest rate per period = i (in this case it is monthly interest rate)
    # (3) number of periods = N (inthis case it is the number of months)
    #
    # Then we have:
    #
    # 1. Equal Total Payment (ETP):
    # principal + interest = (i * A * N) / (1 - (1 + i)**(-N))
    #
    # 2. Equal Principal Payment (EPP):
    # principal + interest = A * (1 + i * (N + 1) / 2)

    ### Rent if we don't buy a house or we don't live in the house we bought
    parser.add_argument('--rent_per_month', type=float, default=30000.0)

    return parser


### Calculate the principal + interest

def ETP(A, i, N):
    '''
    Args:
        A: principal
        i: interest rate per period (in this case it is a monthly interest rate)
        N: number of periods = (in this case it is the number of months)
    Returns:
        the total payment
        
    '''
    return (i * A * N) / (1 - (1 + i)**(-N))


def EPP(A, i, N):
    '''
    Args:
        A: principal
        i: interest rate per period (in this case it is a monthly interest rate)
        N: number of periods = (in this case it is the number of months)
    Returns:
        the total payment
        
    '''
    return A * (1 + i * (N + 1) / 2)


def calculate_principal_and_interest(payment_method, A, i, N):
    if payment_method == 'equal_total_payment':
        principal_and_interest = ETP(principal, monthly_interest_rate, num_periods)
    elif payment_method == 'equal_total_payment':
        principal_and_interest = EPP(principal, monthly_interest_rate, num_periods)
    else:
        raise
    return principal_and_interest


### Calculate the Internal Rate of Return

def IRR(R, N):
    '''
    Args:
        R: total return
        N: number of periods = (in this case it is the number of years)
    Returns:
        the IRR
        
    '''
    return R**(1 / N) - 1


### Plot and visualize

def plot_results(
    loan_term_list, 
    yearly_interest_rate_list,
    loan_dict,
    total_payment_dict,
    total_return_dict,
    IRR_dict,
):
    for loan_term in args.loan_term_list:
        x_list = [] 
        average_loan_per_month_list = []
        total_payment_list = []
        total_margin_list = []
        IRR_list = []
        for yearly_interest_rate in args.yearly_interest_rate_list:
            x_list.append(yearly_interest_rate)
            average_loan_per_month_list.append(loan_dict[(yearly_interest_rate, loan_term)] / (loan_term * 12))
            total_payment_list.append(total_payment_dict[(yearly_interest_rate, loan_term)])
            total_margin_list.append(total_return_dict[(yearly_interest_rate, loan_term)] - total_payment_dict[(yearly_interest_rate, loan_term)])
            IRR_list.append(IRR_dict[(yearly_interest_rate, loan_term)])
        x_array = np.array(x_list)
        average_loan_per_month_array = np.array(average_loan_per_month_list)
        total_payment_array = np.array(total_payment_list)
        total_margin_array = np.array(total_margin_list)
        IRR_array = np.array(IRR_list)

        fig, axs = plt.subplots(2, 2)
        fig.suptitle(f'loan term = {loan_term} years')
        axs[0, 0].plot(x_array, average_loan_per_month_array, 'ro')
        axs[0, 0].set_title(f'average loan per month (loan term = {loan_term} years)')
        axs[0, 1].plot(x_array, total_payment_array, 'ro')
        axs[0, 1].set_title(f'total payment (loan term = {loan_term} years)')
        axs[1, 0].plot(x_array, total_margin_array, 'ro')
        axs[1, 0].set_title(f'total margin (loan term = {loan_term} years)')
        axs[1, 1].plot(x_array, IRR_array, 'ro')
        axs[1, 1].set_title(f'IRR (loan term = {loan_term} years)')

        for ax in axs.flat:
            ax.set(xlabel='yearly interest rate')
            # ax.label_outer()

        fig.tight_layout()
        # plt.savefig(f'loan_term_{loan_term}.png')
        plt.show()



if __name__ == '__main__':
    parser = addParser()
    args = parser.parse_args()

    # down payment
    down_payment = args.house_price * (1 - args.loan_proportion)
    principal = args.house_price - down_payment

    # loan
    loan_dict = {}
    total_payment_dict = {}
    total_return_dict = {}
    IRR_dict = {}

    for yearly_interest_rate in args.yearly_interest_rate_list:
        monthly_interest_rate = yearly_interest_rate / 12

        for loan_term in args.loan_term_list:
            num_periods = loan_term * 12

            # Calculate the total payment using different payment methods 
            # with different interest rates and loan terms
            principal_and_interest = calculate_principal_and_interest(
                args.payment_method,
                principal, 
                monthly_interest_rate, 
                num_periods
            )
            loan_dict[(yearly_interest_rate, loan_term)] = principal_and_interest

            total_payment =  down_payment + principal_and_interest
            total_return = args.price_after_loan_term

            # not sure if the calculation of IRR below is correct in the case of 'B_and_R'
            # because we can further utilize the difference between rents
            # if args.scenario == 'B_and_R':
                # total_payment += args.rent_per_month * num_periods
                # total_return += args.rent_to_others_per_month * num_periods

            total_payment_dict[(yearly_interest_rate, loan_term)] = total_payment
            total_return_dict[(yearly_interest_rate, loan_term)] = total_return

            # If we choose to rent and not buy a house,
            # calculate the required Internal Rate of Return (IRR)
            # to match the return of buying a house.
            rent = args.rent_per_month * loan_term * 12
            IRR_dict[(yearly_interest_rate, loan_term)] = IRR(total_return / (total_payment - rent), loan_term)

    ### Plot and visualize
    plot_results(
        args.loan_term_list, 
        args.yearly_interest_rate_list,
        loan_dict,
        total_payment_dict,
        total_return_dict,
        IRR_dict,
    )
