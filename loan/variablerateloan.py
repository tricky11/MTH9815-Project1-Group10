"""
Loan which can have different rates for each period. The rates are specified using a dictionary.
"""
from loan import Loan


class VariableRateLoan(Loan):
    def __init__(self, notional, rate_dict, term, asset):
        super(VariableRateLoan, self).__init__(notional, None, term, asset)
        self._rate_dict = rate_dict

    @property
    def rate_dict(self):
        return self._rate_dict

    @rate_dict.setter
    def rate_dict(self, rate_dict):
        self._rate_dict = rate_dict

    # The keys in rate_dict are assumed to be in years.
    # period is in months.
    # We convert period to years and check which range it belongs to return the rate for that range.
    def getRate(self, period):
        y = period / 12
        keys = self._rate_dict.keys()
        keys.sort(reverse=True)
        start_period = -1
        for k in keys:
            if y >= k:
                start_period = k
                break
        return self._rate_dict[start_period]
