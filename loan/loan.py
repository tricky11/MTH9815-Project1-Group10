"""

"""
from asset.asset import Asset

__author__ = "Duo Han"


class Loan(object):
    def __init__(self, notional, rate, term, asset):
        self._notional = notional
        self._rate = rate
        self._term = term
        if isinstance(asset, Asset):
            self._asset = asset
        else:
            raise TypeError("asset should be of type Asset. Found : {}".format(type(asset)))

    # 2
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

    def getRate(self, period):
        raise NotImplementedError()

    @property
    def term(self):
        return self._term

    @term.setter
    def term(self, term):
        self._term = term

    @property
    def asset(self):
        return self._asset

    @asset.setter
    def asset(self, asset):
        self._asset = asset

    def monthlyPayment(self, period):
        return self.calcMonthlyPmt(self._notional, self.getRate(period), self._term, period)

    def totalPayment(self):
        return self.monthlyPayment(0) * self._term

    def totalInterest(self):
        return self.totalPayment() - self._notional

    # 3
    # recursive version of interest due
    def interestDue1(self, period):
        if period >= self._term: return 0
        return self.balance1(period - 1) * self.monthlyRate(self._rate)

    # recursive version of principleDue1
    def principleDue1(self, period):
        if period >= self._term: return 0
        return self.monthlyPayment(period) - self.interestDue1(period)

    # recursive version of balance1
    def balance1(self, period):
        if period == 0: return self._notional
        if period >= self._term: return 0
        return self.balance1(period - 1) - self.principleDue1(period)

    # use the formula provided in the slides
    def interestDue2(self, period):
        return self.balance2(period - 1) * self.monthlyRate(self._rate)

    # use the formula provided in the slides
    def principleDue2(self, period):
        return self.monthlyPayment(period) - self.interestDue2(period)

    # use the formula for balance provided in the slides
    def balance2(self, period):
        return self.calcBalance(self._notional, self._rate, self._term, period)

    # 4
    @classmethod
    def calcMonthlyPmt(cls, face, rate, term, period):
        return face * Loan.monthlyRate(rate) / (1 - (1 / (1 + Loan.monthlyRate(rate)) ** (term)))

    @classmethod
    def calcBalance(cls, face, rate, term, period):
        return face * ((1 + Loan.monthlyRate(rate)) ** term - (1 + Loan.monthlyRate(rate)) ** period) / (
            (1 + Loan.monthlyRate(rate)) ** term - 1)

    # 5
    @staticmethod
    def monthlyRate(annualrate):
        return annualrate / 12

    @staticmethod
    def annualRate(monthlyrate):
        return monthlyrate * 12

    def recoveryValue(self, period):
        return 0.6 * self.asset.currentVal(period)

    def equity(self, period):
        return self.asset.currentVal(period) - self.balance2(period)
