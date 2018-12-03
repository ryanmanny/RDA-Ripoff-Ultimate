from .models import PaymentType
from .const import PULLMAN_SALES_TAX


class RipoffCalculator:
    def __init__(self, user, payment_type, base_price, location):
        self.payment_type = payment_type
        self.base_price = base_price
        self.discount_plan = location.discount_plan
        self.rda_plan = user.rda_plan  # Not always used

        self.best_price = None
        self.best_method = None

        self.sticker_price = self._get_sticker_price()
        self._calculate_costs(self.sticker_price)

    def _get_sticker_price(self):
        """Find the credit card price from other payment types, for future calc
        """
        if self.payment_type == PaymentType.RDA:
            return self.base_price / (1 - self.discount_plan.rda_discount_percent)
        elif self.payment_type == PaymentType.CGR:
            return self.base_price / (1 - self.discount_plan.cgr_discount_percent)
        elif self.payment_type == PaymentType.CRD:
            return self.base_price  # Assuming they didn't enter with tax included

    def _rda_real_cost(self, sticker_price):
        return self.rda_plan.real_cost(  # Re-adds proportionate base plan cost
            sticker_price * (1 - self.discount_plan.rda_discount_percent)
        )

    def _cgr_real_cost(self, sticker_price):
        return sticker_price * (1 - self.discount_plan.cgr_discount_percent)

    def _crd_real_cost(self, sticker_price):
        return sticker_price * (1 + PULLMAN_SALES_TAX)

    def _calculate_costs(self, sticker_price):
        """Calculate the actual cost from the sticker price
        """
        self.costs = {
            PaymentType.RDA: self._rda_real_cost(sticker_price),
            PaymentType.CGR: self._cgr_real_cost(sticker_price),
            PaymentType.CRD: self._crd_real_cost(sticker_price),
        }

    def best_value(self):
        """Returns a Tuple of best payment method and best price
        """
        self.best_price, self.best_method = min(
            self.costs.items(),
            key=lambda c: c[1],
        )
        return self.best_price, self.best_method

    def actual_price_paid(self):
        """Returns actual price paid by user
        """
        return self.costs[self.payment_type]

    def ripoff(self):
        """Returns amount of student loans you will have to take out to pay for stupidity
        """
        return self.actual_price_paid() - self.best_value()[0]
