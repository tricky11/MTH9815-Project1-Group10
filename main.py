from loanpool import LoanPool
from standard_tranche import StandardTranche
import waterfall
from structured_securities import StructuredSecurities


def main():
    ss = StructuredSecurities(200000)
    ss.add_tranche(StandardTranche, 0.5, 0.05, 1)
    ss.add_tranche(StandardTranche, 0.5, 0.08, 2)
    waterfall.do_waterfall(LoanPool.create_from_csv("Loans.csv"), ss)


if __name__ == "__main__":
    main()
