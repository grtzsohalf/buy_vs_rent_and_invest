import argparse
import matplotlib.pyplot as plt
import numpy as np



def addParser():
    parser = argparse.ArgumentParser()

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

    ### For the case of Dollar Cost Averaging (DCA) and monthly budget
    parser.add_argument('--monthly_budget', type=float, default=80000.0)

    return parser


### Calculate the principal + interest

def calc_ETP(A, i, N):
    '''
    Args:
        A: principal
        i: interest rate per period (in this case it is a monthly interest rate)
        N: number of periods = (in this case it is the number of months)
    Returns:
        the total payment
        the payment per period
        
    '''
    total_interest = (i * A * N) / (1 - (1 + i)**(-N))
    return total_interest, [total_interest / N for count in range(int(N))]


def calc_EPP(A, i, N):
    '''
    Args:
        A: principal
        i: interest rate per period (in this case it is a monthly interest rate)
        N: number of periods = (in this case it is the number of months)
    Returns:
        the total payment
        the payment per period
        
    '''
    total_interest = A * (1 + i * (N + 1) / 2)
    return total_interest, [A / N + (A * (1 - count / N)) * i for count in range(int(N))] 


def calc_principal_and_interest(payment_method, A, i, N):
    if payment_method == 'equal_total_payment':
        principal_and_interest, loan_per_month_list = \
            calc_ETP(principal, monthly_interest_rate, num_periods)
    elif payment_method == 'equal_total_payment':
        principal_and_interest, loan_per_month_list = \
            calc_EPP(principal, monthly_interest_rate, num_periods)
    else:
        raise
    return principal_and_interest, loan_per_month_list


### Calculate the Internal Rate of Return

def calc_IRR(R, N):
    '''
    Args:
        R: total return
        N: number of periods = (in this case it is the number of years)
    Returns:
        the IRR
        
    '''
    if R > 0.:
        return R**(1 / N) - 1
    else:
        return 0.


def calc_DCA_return(F, i, f, N):
    '''
    Args:
        F: initial fund
        i: monthly rate
        f: fund per month
        N: num_periods
    Returns:
        the return of DCA
        
    '''
    if i == 0.:
        return F + f * N
    else:
        return (F * (1 + i) + f * (1 + 1 / i)) * (1 + i)**(N - 1) \
            - f * (1 + 1 / i)


def calc_DCA_market_IRR(
    down_payment,
    house_return, 
    rent_per_month, 
    loan_per_month,
    num_periods, 
    monthly_budget,
):
    monthly_rate = 0.0
    keep_increase_IRR = True
    rate_increase = 0.0001

    while keep_increase_IRR:

        if monthly_rate > 0.5:
            print("The monthly rate have to be large than 50% !!")
            raise Exception("Don't rent and invest anymore...")
            break

        if monthly_budget < loan_per_month:
            raise Exception("Your monthly budget is less than the monthly loan!!")
        if monthly_budget < rent_per_month:
            raise Exception("Your monthly budget is less than the monthly rent!!")

        with_house_invest_return = calc_DCA_return(
            0.,
            monthly_rate,
            monthly_budget - loan_per_month,
            num_periods
        )
        without_house_invest_return = calc_DCA_return(
            down_payment,
            monthly_rate,
            monthly_budget - rent_per_month,
            num_periods
        )

        if without_house_invest_return > \
                (with_house_invest_return + house_return):
            keep_increase_IRR = False
        else:
            monthly_rate += rate_increase

    return with_house_invest_return, (1 + monthly_rate)**12 - 1


### Plot and visualize

def plot_results(
    loan_term_list, 
    yearly_interest_rate_list,
    loan_dict,
    total_payment_dict,
    total_return_dict,
    IRR_dict,
    DCA_market_IRR_dict
):
    for loan_term in args.loan_term_list:
        x_list = [] 
        average_loan_per_month_list = []
        total_payment_list = []
        total_margin_list = []
        IRR_list = []
        DCA_market_IRR_list = []
        for yearly_interest_rate in args.yearly_interest_rate_list:
            x_list.append(yearly_interest_rate)
            average_loan_per_month_list.append(loan_dict[(yearly_interest_rate, loan_term)] / (loan_term * 12))
            total_payment_list.append(total_payment_dict[(yearly_interest_rate, loan_term)])
            total_margin_list.append(total_return_dict[(yearly_interest_rate, loan_term)] - total_payment_dict[(yearly_interest_rate, loan_term)])
            IRR_list.append(IRR_dict[(yearly_interest_rate, loan_term)])
            DCA_market_IRR_list.append(DCA_market_IRR_dict[(yearly_interest_rate, loan_term)])
        x_array = np.array(x_list)
        average_loan_per_month_array = np.array(average_loan_per_month_list)
        total_payment_array = np.array(total_payment_list)
        total_margin_array = np.array(total_margin_list)
        IRR_array = np.array(IRR_list)
        DCA_market_IRR_array = np.array(DCA_market_IRR_list)

        fig, axs = plt.subplots(2, 2)
        fig.suptitle(f'loan term = {loan_term} years')
        axs[0, 0].plot(x_array, average_loan_per_month_array, 'ro')
        axs[0, 0].set_title(f'average loan per month (loan term = {loan_term} years)')
        axs[0, 1].plot(x_array, total_margin_array, 'ro')
        axs[0, 1].set_title(f'total margin (loan term = {loan_term} years)')
        axs[1, 0].plot(x_array, IRR_array, 'ro')
        axs[1, 0].set_title(f'needed IRR (loan term = {loan_term} years)')
        axs[1, 1].plot(x_array, DCA_market_IRR_array, 'ro')
        axs[1, 1].set_title(f'needed market IRR (DCA) (loan term = {loan_term} years)')

        for ax in axs.flat:
            ax.set(xlabel='yearly interest rate')
            # ax.label_outer()

        fig.tight_layout()
        # plt.savefig(f'loan_term_{loan_term}.png')
        plt.show()



if __name__ == '__main__':
    parser = addParser()
    args = parser.parse_args()

    # Down payment
    down_payment = args.house_price * (1 - args.loan_proportion)
    principal = args.house_price - down_payment

    # Loan
    loan_dict = {}
    total_payment_dict = {}
    total_return_dict = {}
    IRR_dict = {}
    DCA_market_IRR_dict = {}

    for yearly_interest_rate in args.yearly_interest_rate_list:
        monthly_interest_rate = yearly_interest_rate / 12

        for loan_term in args.loan_term_list:
            num_periods = loan_term * 12

            # Calculate the total payment using different payment methods 
            # with different interest rates and loan terms
            principal_and_interest, loan_per_month_list = calc_principal_and_interest(
                args.payment_method,
                principal, 
                monthly_interest_rate, 
                num_periods
            )
            loan_dict[(yearly_interest_rate, loan_term)] = principal_and_interest

            house_payment =  down_payment + principal_and_interest
            house_return = args.price_after_loan_term

            # If we choose to rent and not buy a house,
            # calculate the required Internal Rate of Return (IRR)
            # to match the return of buying a house.
            rent = args.rent_per_month * num_periods
            IRR_dict[(yearly_interest_rate, loan_term)] = \
                calc_IRR(house_return / (house_payment - rent), loan_term)

            # For the case of Dollar Cost Averaging (DCA) and monthly budget
            # To simplify the computation, we assume loan_per_month to be the
            # average over the loan term
            invest_return, DCA_market_IRR = calc_DCA_market_IRR(
                down_payment,
                house_return, 
                args.rent_per_month, 
                principal_and_interest / num_periods,
                num_periods, 
                args.monthly_budget,
            )
            DCA_market_IRR_dict[(yearly_interest_rate, loan_term)] = DCA_market_IRR

            total_payment_dict[(yearly_interest_rate, loan_term)] = down_payment + args.monthly_budget * num_periods
            total_return_dict[(yearly_interest_rate, loan_term)] = house_return + invest_return

    ### Plot and visualize
    plot_results(
        args.loan_term_list, 
        args.yearly_interest_rate_list,
        loan_dict,
        total_payment_dict,
        total_return_dict,
        IRR_dict,
        DCA_market_IRR_dict,
    )
