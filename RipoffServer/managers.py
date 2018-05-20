from django.db import models

from calculate_ripoff import calculate_simple_ripoff

class RipOffManager(models.Manager):
    def create_ripoff(self, **kwargs):
        ripoff = calculate_simple_ripoff(**kwargs)

        return self.objects.create(ripoff=ripoff, **kwargs)
