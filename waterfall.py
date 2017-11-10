import multiprocessing

import numpy as np


def do_waterfall(loan_pool, structured_securities):
    time = 0
    structured_securities.reset()
    loan_pool.reset()
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


def run_simulation_parallel(loan_pool, structured_securities, nsim, num_processes):
    input_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()

    for i in range(num_processes):
        input_queue.put((simulate_waterfall, (loan_pool, structured_securities, nsim / num_processes)))

    for i in range(num_processes):
        multiprocessing.Process(target=doWork, args=(input_queue, output_queue)).start()

    res = []
    while len(res) < num_processes:
        r = output_queue.get()
        res.append(r)

    # Aggregate results
    results = reduce(lambda x, y: [(x[0][0] + y[0][0], x[0][1] + y[0][1]), (x[1][0] + y[1][0], x[1][1] + y[1][1])], res,
                     [(0.0, 0.0), (0.0, 0.0)])
    results = [(results[0][0] / len(res), results[0][1] / len(res)),
               (results[1][0] / len(res), results[1][1] / len(res))]
    return results


def doWork(input, output):
    while True:
        try:
            f, args = input.get(timeout=1)
            res = f(*args)
            output.put(res)
            print "Process finished"
        except:
            break


def calculate_yield(a, d):
    return ((7 / (1 + 0.08 * np.exp(-0.19 * a / 12))) + (0.019 * np.sqrt(a * abs(d) * 100 / 12))) / 100


def get_new_tranche_rate(old_rate, y, coeff):
    return old_rate + coeff * (y - old_rate)


def get_diff(notionals, old_rates, new_rates):
    return sum([notional * abs(new_rate / old_rate - 1) for notional, old_rate, new_rate in
                zip(notionals, old_rates, new_rates)]) / sum(notionals)


def run_monte(loan_pool, structured_securities, tolerance, nsim):
    notionals = [tranche.notional for tranche in structured_securities.tranches]
    old_rates = [tranche.rate for tranche in structured_securities.tranches]
    while True:
        simulation_results = run_simulation_parallel(loan_pool, structured_securities, nsim, 20)
        yields = [calculate_yield(a, d) for (a, d) in simulation_results]
        new_a_rate = get_new_tranche_rate(old_rates[0], yields[0], 1.2)
        new_b_rate = get_new_tranche_rate(old_rates[1], yields[1], 0.8)
        diff = get_diff(notionals, old_rates, [new_a_rate, new_b_rate])
        if diff < tolerance:
            break
        else:
            old_rates = [new_a_rate, new_b_rate]
            # Update rates.
            for tranche, new_rate in zip(structured_securities.tranches, old_rates):
                tranche.rate = new_rate
        print "Outer simulation : diff = {}".format(diff)
        print "Outer simulation : rates = {}".format(old_rates)
    return new_a_rate, new_b_rate
