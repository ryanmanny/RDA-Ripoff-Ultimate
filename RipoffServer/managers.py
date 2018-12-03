from django.db import models
from django.db.models import F, Sum


class RipoffSet(models.QuerySet):
    def add_total_ripoff(self):
        """Adds aggregated total field to QuerySet
        """
        return self.aggregate(
            total_ripoff=Sum('ripoff_amount')
        )


class UserSet(models.QuerySet):
    pass


class UserManager(models.Manager):
    def get_queryset(self):
        print("Adding select_related discount_plan to UserSet")
        return super().get_queryset().select_related('rda_plan')


class LocationSet(models.QuerySet):
    pass


class LocationManager(models.Manager):
    def get_queryset(self):
        print("Adding select_related discount_plan to LocationSet")
        return super().get_queryset().select_related('discount_plan')
