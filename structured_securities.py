from enum import Enum


class Mode(Enum):
    sequential = 1
    pro_rate = 2


class StructuredSecurities(object):
    def __init__(self, notional):
        self._notional = notional
        self._tranches = []
        self._mode = Mode.sequential
        self._reserve = 0

    def add_tranche(self, tranche):
        self._tranches.append(tranche)

    def set_mode(self, mode):
        self._mode = mode

    def make_payments(self, cash_amount):
        pass

    def get_waterfall(self):
        pass
