from django.db import models


class RipoffManager(models.Manager):
    pass

    # TODO: Aggregate Querysets with total

    # def get_running_total(self):
    #     return sum(ripoff.ripoff_amount for ripoff in self.objects.all())
