import waterfall
from loanpool import LoanPool
from standard_tranche import StandardTranche
from structured_securities import StructuredSecurities


def main():
    # Create a structured security
    abs = StructuredSecurities(20000000)
    abs.add_tranche(StandardTranche, 0.5, 0.05, 1)
    abs.add_tranche(StandardTranche, 0.5, 0.08, 2)

    loan_pool = LoanPool.create_from_csv("Loans.csv")

    # Suggested simulation in the Project
    # fair_coupon_rates = waterfall.run_monte(loan_pool, abs, 0.005, 2000)

    # Faster simulation just for verifying if the program runs properly
    fair_coupon_rates = waterfall.run_monte(loan_pool, abs, 0.1, 20)

    print "Fair coupon rates for tranches are: {}".format(fair_coupon_rates)

    # Run the waterfall with fair coupon rates and save waterfall to csv.
    fair_abs = StructuredSecurities(20000000)
    fair_abs.add_tranche(StandardTranche, 0.5, fair_coupon_rates[0], 1)
    fair_abs.add_tranche(StandardTranche, 0.5, fair_coupon_rates[1], 2)
    run_single_waterfall(loan_pool, fair_abs)
    print "Amount left in reserve account : {}".format(fair_abs.reserve)


def run_single_waterfall(loan_pool, ss):
    print "Waterfall results:"
    waterfall_results = waterfall.do_waterfall(loan_pool, ss)
    [tranche_results[0].to_csv("Liabilities_{}.csv".format(i)) for i, tranche_results in
     enumerate(waterfall_results)]
    print "IRR: {}".format([tranche_results[1] for tranche_results in waterfall_results])
    print "AL: {}".format([tranche_results[2] for tranche_results in waterfall_results])
    print "DIRR: {}".format([tranche_results[3] for tranche_results in waterfall_results])
    print "Rating: {}".format([tranche_results[4] for tranche_results in waterfall_results])


if __name__ == "__main__":
    main()
