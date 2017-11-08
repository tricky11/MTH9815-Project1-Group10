"""
Abstract base class for Cars.
"""
from asset.asset import Asset


class Car(Asset):
    def annualDeprRate(self):
        raise NotImplementedError()
