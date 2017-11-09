import waterfall
from loanpool import LoanPool
from standard_tranche import StandardTranche
from structured_securities import StructuredSecurities


def main():
    ss = StructuredSecurities(20000000)
    ss.add_tranche(StandardTranche, 0.5, 0.05, 1)
    ss.add_tranche(StandardTranche, 0.5, 0.08, 2)

    loan_pool = LoanPool.create_from_csv("Loans.csv")
    fair_coupon_rates = waterfall.run_monte(loan_pool, ss, 0.1, 20)
    print "Fair coupon rates for tranches are: {}".format(fair_coupon_rates)
    fair_ss = StructuredSecurities(20000000)
    fair_ss.add_tranche(StandardTranche, 0.5, fair_coupon_rates[0], 1)
    fair_ss.add_tranche(StandardTranche, 0.5, fair_coupon_rates[1], 2)
    print "Amount left in reserve account : {}".format(ss.reserve)
    run_single_waterfall(loan_pool, fair_ss)


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
