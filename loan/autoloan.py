"""
Loan on an automobile. Assumed to be fixed rate.
"""
from q2_2.asset.car.car import Car
from q2_2.loan.fixedrateloan import FixedRateLoan


class AutoLoan(FixedRateLoan):
    def __init__(self, notional, rate, term, car):
        if isinstance(car, Car):
            super(AutoLoan, self).__init__(notional, rate, term, car)
        else:
            raise TypeError("car should be of type Car. Found : {}".format(type(car)))
