from enum import Enum

"""
Represents a Structured Security and holds all its tranches. 
Contains methods for adding new tranches and making payments.

Call reset when re-using this class after making any payments.
"""


class Mode(Enum):
    """
    Enum for setting the mode of principal payments for a Structured Security.
    """
    sequential = 1
    pro_rata = 2


class StructuredSecurities(object):
    def __init__(self, notional):
        self._notional = notional
        # Convert list of tranches to pandas dataframe?
        self._tranches = []
        self._mode = Mode.sequential
        self._reserve = 0

    def add_tranche(self, tranche_class, percent_notional, rate, subordination):
        # TODO(harishchandra): Instead of appending and sorting, insert the new tranche at correct position.
        tranche = tranche_class(percent_notional * self._notional, rate, subordination)
        self._tranches.append(tranche)
        self._tranches = sorted(self._tranches, key=lambda t: t.subordination)

    def set_mode(self, mode):
        if isinstance(mode, Mode):
            self._mode = mode
        else:
            raise TypeError("'mode' has to be one of Mode.sequential or Mode.pro_rata. Found: " + str(type(mode)))

    def increase_time_period(self):
        [tranche.increase_time_period() for tranche in self._tranches if tranche.notional_balance() > 0]

    def make_payments(self, cash_amount):
        """
        Combine the reserve cash from previous periods to the new amount available this period.
        Make interest payments to all tranches.
        Make principal payments to all tranches as per the mode set on this security.
        Add remaining cash to reserve account.

        :param cash_amount: The new amount available to make payments this period.
        :return: None
        """
        # Use the reserve amount from previous iteration.
        cash_amount += self._reserve
        self._reserve = 0

        # Make interest payments first.
        # TODO: convert these to reduce operations
        for tranche in self._tranches:
            available_interest_amount = min(cash_amount, tranche.interest_due())
            if available_interest_amount > 0:
                tranche.make_interest_payment(available_interest_amount)
                cash_amount -= available_interest_amount

        # Make principal payments according to mode.
        if self._mode == Mode.pro_rata:
            total_notional = sum([tranche.notional for tranche in self._tranches])
            principals_due = [tranche.notional * cash_amount / total_notional for tranche in self._tranches]
            # TODO: convert these to reduce operations
            for i, tranche in enumerate(self._tranches):
                available_principal_amount = min(principals_due[i], tranche.notional_balance())
                if available_principal_amount > 0:
                    tranche.make_principal_payment(available_principal_amount)
                    cash_amount -= available_principal_amount
        elif self._mode == Mode.sequential:
            # TODO: convert these to reduce operations
            for tranche in self._tranches:
                available_principal_amount = min(cash_amount, tranche.notional_balance())
                if available_principal_amount > 0:
                    tranche.make_principal_payment(available_principal_amount)
                    cash_amount -= available_principal_amount
        else:
            # This should never occur since we check for valid mode while setting it.
            raise TypeError("Unknown mode: " + str(self._mode))

        # Store the excess cash in reserve account for use in next iteration.
        self._reserve += cash_amount

    def get_waterfall(self):
        return [(tranche.transactions, tranche.irr(), tranche.al(), tranche.dirr(), tranche.rating()) for tranche in
                self._tranches]

    @property
    def reserve(self):
        return self._reserve

    @property
    def tranches(self):
        return self._tranches

    def reset(self):
        """
        Reset all tranches and set reserve cash to 0.

        :return: None
        """
        [tranche.reset() for tranche in self._tranches]
        self._reserve = 0
