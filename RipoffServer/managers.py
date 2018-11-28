from django.db import models
from django.db.models import F, Sum


class RipoffSet(models.QuerySet):
    def add_total_ripoff(self):
        """Adds aggregated total field to QuerySet
        """
        return self.aggregate(
            total_ripoff=Sum('ripoff_amount')
        )
