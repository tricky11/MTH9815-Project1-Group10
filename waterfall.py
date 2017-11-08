def do_waterfall(loan_pool, structured_securities):
    pass


def simulate_waterfall(loan_pool, structured_securities, nsim):
    results = [do_waterfall(loan_pool, structured_securities) for i in range(nsim)]
    sum_results = reduce(lambda x, y: (x[0] + y[0], x[1] + y[1]), results, (0, 0))
    return sum_results[0] / nsim, sum_results[1] / nsim


def calculate_yield(a, d):
    return 0


def get_new_tranche_rate(old_rate, y, coeff):
    return old_rate + coeff * (y - old_rate)


def get_diff(nA, nB, prevARate, newARate, prevBRate, newBRate):
    return 0


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
