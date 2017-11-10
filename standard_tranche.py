from tranche import Tranche

"""
A standard tranche which makes both interest and principal payments.
Can only make 1 interest or principal payment each period.

Call reset if an object needs to be reused.
"""


class StandardTranche(Tranche):
    def __init__(self, notional, rate, subordination):
        super(StandardTranche, self).__init__(notional, rate, subordination)

        self._time = 0
        self._interest_paid = False
        self._principal_paid = False
        self._transactions.loc[0] = [0, 0, 0, 0, notional]

    def increase_time_period(self):
        """
        Increase time period by 1.
        Update the previous periods ending notional balance.
        Create an empty entry in the transactions DataFrame for the new time period.

        :return: int: The new time period.
        """
        self._transactions.loc[self._time]["notional_balance"] = self.notional_balance()
        self._time += 1
        self._transactions.loc[self._time] = [0, 0, 0, 0, 0]
        self._interest_paid = False
        self._principal_paid = False
        return self._time

    def make_principal_payment(self, principal_payment):
        """
        Update principal and total payments and set flag.

        :param principal_payment: float: The amount of principal paid in this time period.
        :return: None
        """
        if self._principal_paid:
            raise ValueError("Principal has already been paid for this time period.")
        if self.notional_balance() == 0:
            raise ValueError("Notional balance is 0. Cannot make any more principal payments.")
        self._transactions.loc[self._time]["principal_payment"] = principal_payment
        self._transactions.loc[self._time]["total_payment"] += principal_payment
        self._principal_paid = True

    def make_interest_payment(self, interest_payment):
        """
        Update interest and total payments and set flag.

        :param interest_payment: float: The amount of interest paid in this time period.
        :return: None
        """
        if self._interest_paid:
            raise ValueError("Interest has already been paid for this time period.")
        interest_amount_due = self.interest_due()
        if interest_amount_due == 0:
            raise ValueError("Interest due is 0. Cannot make any more interest payments.")
        self._transactions.loc[self._time]["interest_payment"] = interest_payment
        self._transactions.loc[self._time]["total_payment"] += interest_payment
        self._transactions.loc[self._time]["interest_shortfall"] = interest_amount_due - interest_payment
        self._interest_paid = True

    def notional_balance(self):
        """
        Calculate notional balance pending at this instant (including all principal payments and interest shortfalls.)

        :return: float: The notional balance.
        """
        return self._notional \
               - self._transactions['principal_payment'].sum() \
               + self._transactions['interest_shortfall'].sum()

    def interest_due(self):
        """
        Calculate interest due in this period using the notional balance.
        This should be called before making any payments in this time period.

        :return: float: The interest due in this time period.
        """
        return self.notional_balance() * self._rate / 12

    def reset(self):
        """
        Reset time and all flags. Remove all entries from transaction DataFrame.

        :return: None
        """
        self._time = 0
        self._interest_paid = False
        self._principal_paid = False
        self._transactions.drop(self._transactions.index, inplace=True)
        self._transactions.loc[0] = [0, 0, 0, 0, self._notional]
