import numpy as np
import pandas as pd


def do_waterfall(loan_pool, structured_securities):
    t = 0
    while loan_pool.get_active_loan_count(t) > 0:
        t += 1
        structured_securities.increase_time_period()
        amount_received = loan_pool.get_total_payment_due(t)
        structured_securities.make_payments(amount_received)
    liabilities_transactions = structured_securities.get_waterfall()
    [tranche_transactions.to_csv("Liabilities_{}.csv".format(i)) for i, tranche_transactions in
     enumerate(liabilities_transactions)]
    return liabilities_transactions


def simulate_waterfall(loan_pool, structured_securities, nsim):
    results = [do_waterfall(loan_pool, structured_securities) for i in range(nsim)]
    sum_results = reduce(lambda x, y: (x[0] + y[0], x[1] + y[1]), results, (0, 0))
    return sum_results[0] / nsim, sum_results[1] / nsim


def calculate_yield(a, d):
    return ((7 / (1 + 0.08 * np.exp(-0.19 * a / 12))) + (0.019 * np.sqrt(a * d * 100 / 12))) / 100


def get_new_tranche_rate(old_rate, y, coeff):
    return old_rate + coeff * (y - old_rate)


def get_diff(nA, nB, prevARate, newARate, prevBRate, newBRate):
    return (nA * abs(newARate / prevARate - 1) + nB * abs(newBRate / prevBRate - 1)) / (nA + nB)


def run_monte(loan_pool, structured_securities, tolerance, nsim):
    old_a_rate = 0.08
    old_b_rate = 0.05
    notional_a = 1
    notional_b = 1
    while True:
        a, d = simulate_waterfall(loan_pool, structured_securities, nsim)
        y = calculate_yield(a, d)
        new_a_rate = get_new_tranche_rate(old_a_rate, y, 1.2)
        new_b_rate = get_new_tranche_rate(old_b_rate, y, 0.8)
        if get_diff(notional_a, notional_b, old_a_rate, new_a_rate, old_b_rate, new_b_rate) < tolerance:
            break
        else:
            old_a_rate = new_a_rate
            old_b_rate = new_b_rate
    return new_a_rate, new_b_rate
