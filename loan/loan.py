"""

"""
from asset.asset import Asset


class Loan(object):
    def __init__(self, notional, rate, term, asset):
        self._notional = notional
        self._rate = rate
        self._term = term
        self._defaulted = False

        if isinstance(asset, Asset):
            self._asset = asset
        else:
            raise TypeError("asset should be of type Asset. Found : {}".format(type(asset)))

    def check_default(self, time, random_number):
        if self._defaulted:
            return 0
        elif random_number == 0:
            self._defaulted = True
            self._notional = 0
            return self.asset.currentVal(time)
        else:
            return 0

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

    @property
    def defaulted(self):
        return self._defaulted

    def monthlyPayment(self, period):
        return self.calcMonthlyPmt(self._notional, self.getRate(period), self._term, period)

    def totalPayment(self):
        return self.monthlyPayment(0) * self._term

    def totalInterest(self):
        return self.totalPayment() - self._notional

    def interestDue(self, period):
        return self.balance(period - 1) * self.monthlyRate(self._rate)

    def principleDue(self, period):
        return self.monthlyPayment(period) - self.interestDue(period)

    def balance(self, period):
        return self.calcBalance(self._notional, self._rate, self._term, period) if not self._defaulted else 0

    @classmethod
    def calcMonthlyPmt(cls, face, rate, term, period):
        return face * Loan.monthlyRate(rate) / (1 - (1 / (1 + Loan.monthlyRate(rate)) ** (term)))

    @classmethod
    def calcBalance(cls, face, rate, term, period):
        return face * ((1 + Loan.monthlyRate(rate)) ** term - (1 + Loan.monthlyRate(rate)) ** period) / (
            (1 + Loan.monthlyRate(rate)) ** term - 1)

    @staticmethod
    def monthlyRate(annualrate):
        return annualrate / 12

    @staticmethod
    def annualRate(monthlyrate):
        return monthlyrate * 12

    def recoveryValue(self, period):
        return 0.6 * self.asset.currentVal(period)

    def equity(self, period):
        return self.asset.currentVal(period) - self.balance(period)
