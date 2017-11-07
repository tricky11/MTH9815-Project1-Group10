class Tranche(object):
    def __init__(self, notional, rate, subordination):
        self._notional = notional
        self._rate = rate
        self._subordination = subordination

    def irr(self):
        pass

    def al(self):
        pass

    def dirr(self):
        pass

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
