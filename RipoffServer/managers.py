from django.db import models


class RipoffManager(models.Manager):
    def get_running_total(self):
        return sum(ripoff.ripoff_amount for ripoff in self.objects.all())
