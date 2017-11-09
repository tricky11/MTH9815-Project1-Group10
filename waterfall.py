import numpy as np


def do_waterfall(loan_pool, structured_securities):
    time = 0
    while loan_pool.get_active_loan_count(time) > 0:
        time += 1
        structured_securities.increase_time_period()
        recovery_amount = loan_pool.check_defaults(time)
        payments_received = loan_pool.get_total_payment_due(time)
        structured_securities.make_payments(payments_received + recovery_amount)
    return structured_securities.get_waterfall()


def simulate_waterfall(loan_pool, structured_securities, nsim):
    als = ([], [])
    dirrs = ([], [])
    for i in range(nsim):
        result = do_waterfall(loan_pool, structured_securities)
        for j, tranche in enumerate(result):
            if not np.isinf(tranche[2]):
                als[j].append(tranche[2])
            dirrs[j].append(tranche[3])
    return ((np.mean(als[0]), np.mean(dirrs[0])), (np.mean(als[1]), np.mean(dirrs[1])))


def calculate_yield(a, d):
    return ((7 / (1 + 0.08 * np.exp(-0.19 * a / 12))) + (0.019 * np.sqrt(a * d * 100 / 12))) / 100


def get_new_tranche_rate(old_rate, y, coeff):
    return old_rate + coeff * (y - old_rate)


def get_diff(nA, nB, prevARate, newARate, prevBRate, newBRate):
    return (nA * abs(newARate / prevARate - 1) + nB * abs(newBRate / prevBRate - 1)) / (nA + nB)


def run_monte(loan_pool, structured_securities, tolerance, nsim):
    old_a_rate = 0.05
    old_b_rate = 0.08
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
