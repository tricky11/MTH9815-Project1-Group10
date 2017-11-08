import uuid

import numpy as np
from pandas import DataFrame


class Tranche(object):
    def __init__(self, notional, rate, subordination):
        self._notional = notional
        self._rate = rate
        self._subordination = subordination
        self._id = uuid.uuid4()
        self._transactions = DataFrame(
            columns=['principal_payment', 'interest_payment', 'interest_shortfall', 'recovery', 'total_payment',
                     'notional_balance'], dtype=float)

    def irr(self):
        return np.irr([-self.notional, self._transactions['notional_balance'][1:]])

    def al(self):
        return (sum([x * y for x, y in zip(self._transactions['notional_balance'][1:],
                                           range(1, self._transactions.size()))]) - self.notional) / self.notional

    def dirr(self):
        return self.rate - self.irr()

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
    def id(self):
        return self._id

    @property
    def transactions(self):
        return self._transactions
