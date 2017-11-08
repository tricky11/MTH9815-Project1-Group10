"""
Base class for Asset. Contains methods for valuing an asset.
"""


class Asset(object):
    def __init__(self, val):
        self._val = val
        self._rate = 0.1

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, val):
        self._val = val

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, _rate):
        self._rate = _rate

    # Get monthly depreciation Function
    def annualDeprRate(self):
        raise NotImplementedError()

    # Get monthly depreciation Function
    def monthlyDeprRate(self):
        return self.annualDeprRate() / 12.

    # Calculating current value of the asset
    def currentVal(self, period):
        return self._val * (1 - self.monthlyDeprRate()) ** period
