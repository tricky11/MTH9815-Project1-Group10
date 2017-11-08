"""
Loan which has a fixed rate for all periods.
"""
from loan import Loan


class FixedRateLoan(Loan):
    def getRate(self, period):
        return self.monthlyRate(self.rate)
