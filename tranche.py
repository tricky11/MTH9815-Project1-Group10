import numpy as np
from pandas import DataFrame

"""
Base class for a tranche in a Structured Security. 
Contains methods for calculating waterfall metrics.
"""

class Tranche(object):
    def __init__(self, notional, rate, subordination):
        self._notional = notional
        self._rate = rate
        self._subordination = subordination
        self._transactions = DataFrame(
            columns=['principal_payment', 'interest_payment', 'interest_shortfall', 'total_payment',
                     'notional_balance'], dtype=float)

    def irr(self):
        payments = self._transactions['total_payment'][1:].tolist()
        payments.insert(0, -self.notional)
        return np.irr(payments) * 12

    def al(self):
        ending_balance = self._transactions['notional_balance'].iloc[-1]
        return ((sum([x * y for x, y in zip(self._transactions['notional_balance'].tolist(), range(
            self._transactions.size + 1))]) - self.notional) / self.notional) if ending_balance == 0 else np.inf

    def dirr(self):
        return self.rate - self.irr()

    def rating(self):
        dirr_bps = self.dirr() / 100
        if dirr_bps <= 0.06:
            return "AAA"
        if dirr_bps <= 0.67:
            return "AA1"
        if dirr_bps <= 1.3:
            return "AA2"
        if dirr_bps <= 2.7:
            return "AA3"
        if dirr_bps <= 5.2:
            return "A1"
        if dirr_bps <= 8.9:
            return "A2"
        if dirr_bps <= 13:
            return "A3"
        if dirr_bps <= 19:
            return "BAA1"
        if dirr_bps <= 27:
            return "BAA2"
        if dirr_bps <= 46:
            return "BAA3"
        if dirr_bps <= 72:
            return "BA1"
        if dirr_bps <= 106:
            return "BA2"
        if dirr_bps <= 143:
            return "BA3"
        if dirr_bps <= 183:
            return "B1"
        if dirr_bps <= 231:
            return "B2"
        if dirr_bps <= 311:
            return "B3"
        if dirr_bps <= 2500:
            return "CAA"
        if dirr_bps <= 10000:
            return "CA"

    @property
    def notional(self):
        return self._notional

    @notional.setter
    def notional(self, notional):
        self._notional = notional

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, rate):
        self._rate = rate

    @property
    def subordination(self):
        return self._subordination

    @subordination.setter
    def subordination(self, subordination):
        self._subordination = subordination

    @property
    def transactions(self):
        return self._transactions
