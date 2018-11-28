from abc import ABC

from .models import PaymentType


class RipoffCalculator:
    # TODO: Evaluate overcomplicated factory idea
    # def __new__(cls, *args, **kwargs):
    #     payment_type = kwargs.pop('payment_type')
    #     return super().__new__(
    #         {
    #             PaymentType.RDA: RDARipoffCalculator,
    #             PaymentType.CGR: CGRRipoffCalculator,
    #             PaymentType.CRD: CRDRipoffCalculator,
    #         }[payment_type],
    #         *args, **kwargs,
    #     )

    def __init__(self, *args, **kwargs):
        self.payment_type = kwargs.pop('payment_type')
        self.base_price = kwargs.pop('base_price')
        self.discount_plan = kwargs.pop('discount_plan')
        self.rda_plan = kwargs.pop('rda_plan')  # Not always used

        self._calculate_costs()

    def _calculate_costs(self):
        self.disc

    def _best_value(self):
        pass

    def _price_paid(self):
        pass

    def ripoff(self):
        return self._price_paid() - self._best_value()