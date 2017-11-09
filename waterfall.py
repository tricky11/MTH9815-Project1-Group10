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
        print "Inner simulation : {}".format(i)
    return [(np.mean(tranche_als), np.mean(tranche_dirrs)) for tranche_als, tranche_dirrs in zip(als, dirrs)]


def calculate_yield(a, d):
    return ((7 / (1 + 0.08 * np.exp(-0.19 * a / 12))) + (0.019 * np.sqrt(a * d * 100 / 12))) / 100


def get_new_tranche_rate(old_rate, y, coeff):
    return old_rate + coeff * (y - old_rate)


def get_diff(notionals, old_rates, new_rates):
    return sum([notional * abs(new_rate / old_rate - 1) for notional, old_rate, new_rate in
                zip(notionals, old_rates, new_rates)]) / sum(notionals)


def run_monte(loan_pool, structured_securities, tolerance, nsim):
    notionals = structured_securities.tranche_notionals()
    old_rates = structured_securities.tranche_rates()
    while True:
        simulation_results = simulate_waterfall(loan_pool, structured_securities, nsim)
        yields = [calculate_yield(a, d) for (a, d) in simulation_results]
        new_a_rate = get_new_tranche_rate(old_rates[0], yields[0], 1.2)
        new_b_rate = get_new_tranche_rate(old_rates[1], yields[1], 0.8)
        diff = get_diff(notionals, old_rates, [new_a_rate, new_b_rate])
        if diff < tolerance:
            break
        else:
            old_rates = [new_a_rate, new_b_rate]
        print "Outer simulation : diff = {}".format(diff)
        print "Outer simulation : rates = {}".format(old_rates)
    return new_a_rate, new_b_rate
