"""
Collection of loans and methods to get aggregated values over entire collection.
"""
import numpy as np
import pandas as pd

from asset.car.lexus import Lexus
from loan.autoloan import AutoLoan


class LoanPool(object):
    def __init__(self, loans):
        self._loans = loans

    def check_defaults(self, time):
        return sum(
            [loan.check_default(time, np.random.randint(int(1 / LoanPool.get_default_probability(time)))) for loan in
             self._loans])

    @staticmethod
    def get_default_probability(time):
        if time <= 10:
            return 0.0005
        if time <= 59:
            return 0.001
        if time <= 120:
            return 0.002
        if time <= 180:
            return 0.004
        if time <= 210:
            return 0.002
        else:
            return 0.001

    @property
    def loans(self):
        return self._loans

    @loans.setter
    def loans(self, loans):
        self._loans = loans

    def add_loan(self, loan):
        self._loans.append(loan)

    def get_total_principal(self):
        return sum([loan.notional for loan in self._loans])

    def get_total_balance(self, period):
        return sum([loan.balance(period) for loan in self._loans])

    def get_total_principal_due(self, period):
        return sum([loan.principal(period) for loan in self._loans])

    def get_total_interest_due(self, period):
        return sum([loan.interest(period) for loan in self._loans])

    def get_total_payment_due(self, period):
        return sum([loan.monthlyPayment(period) for loan in self._loans if not loan.defaulted])

    def get_active_loan_count(self, period):
        return sum([loan.balance(period) > 0 for loan in self._loans])

    def get_weighted_average_maturity(self):
        return sum([loan.notional * loan.term for loan in self._loans]) / self.get_total_principal()

    def get_weighted_average_rate(self):
        return sum([loan.notional * loan.rate for loan in self._loans]) / self.get_total_principal()

    @staticmethod
    def create_from_csv(filename):
        df = pd.read_csv(filename, index_col=["Loan #"])
        return LoanPool([AutoLoan(loan[0], loan[1], loan[2], Lexus(loan[3])) for loan in
                         df.as_matrix(columns=['Balance', 'Rate', 'Term', 'Asset Value'])])
