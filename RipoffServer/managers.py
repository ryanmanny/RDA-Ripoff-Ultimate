from django.db import models


class RipoffManager(models.Manager):
    def create_ripoff(self, **kwargs):
        def calculate_simple_ripoff(base_cost, payment_type, discount_plan):
            # TODO: UNSTUB
            return base_cost

        ripoff = calculate_simple_ripoff(**kwargs)

        return self.objects.create(ripoff=ripoff, **kwargs)
