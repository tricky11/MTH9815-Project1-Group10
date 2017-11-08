"""
Abstract base class for Assets of House category.
"""
from q2_2.asset.asset import Asset


class HouseBase(Asset):
    def annualDeprRate(self):
        raise NotImplementedError()
