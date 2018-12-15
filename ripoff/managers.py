from django.db import models
from django.contrib.auth import models as auth_models

from django.db.models import F, Sum


class RipoffSet(models.QuerySet):
    def add_total_ripoff(self):
        """Adds aggregated total field to QuerySet
        """
        return self.aggregate(
            total_ripoff=Sum('ripoff_amount')
        )


class RipoffManager(models.Manager):
    pass


class SiteUserManager(auth_models.UserManager):
    def get_queryset(self):
        print("Adding select_related discount_plan to SiteUserSet")
        return super().get_queryset().select_related('rda_plan')


class LocationSet(models.QuerySet):
    pass


class LocationManager(models.Manager):
    def get_queryset(self):
        print("Adding select_related discount_plan to LocationSet")
        return super().get_queryset().select_related('discount_plan')
