"""
Abstract base class for Cars.
"""
from q2_2.asset.asset import Asset


class Car(Asset):
    def annualDeprRate(self):
        raise NotImplementedError()
