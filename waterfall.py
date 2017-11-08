def do_waterfall(loan_pool, structured_securities):
    pass


def simulate_waterfall(loan_pool, structured_securities, nsim):
    results = [do_waterfall(loan_pool, structured_securities) for i in range(nsim)]
    sum_results = reduce(lambda x, y: (x[0] + y[0], x[1] + y[1]), results, (0, 0))
    return sum_results[0] / nsim, sum_results[1] / nsim
