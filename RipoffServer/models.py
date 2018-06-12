from django.db import models
from django.contrib.auth import models as auth_models

from RipoffServer.managers import RipoffManager

from enum import Enum


# MODELS
class SiteUser(auth_models.User):
    rda_plan = models.IntegerField()  # Level 0-3


class Product(models.Model):
    name = models.CharField(max_length=40)
    # Made its own model for further extensibility later


class Location(models.Model):
    name = models.CharField(max_length=40)
    discount_plan = models.ForeignKey('DiscountPlan', null=True, on_delete=models.SET_NULL)


class PaymentType(Enum):
    CRD = "Credit Card"
    CGR = "Cougar Cash"
    RDA = "RDA"


class DiscountPlan(models.Model):
    # Percentage discounts applied to different purchase methods
    rda_discount = models.FloatField(verbose_name="RDA Discount")
    cc_discount = models.FloatField(verbose_name="Cougar Cash Discount")


class Ripoff(models.Model):
    objects = RipoffManager()  # Supplies with create_ripoff function that dynamically calculates ripoff

    date = models.DateTimeField(auto_now=True)

    user = models.ForeignKey('SiteUser', null=True, on_delete=models.SET_NULL)
    product = models.CharField(max_length=40)
    location = models.ForeignKey('Location', on_delete=None)
    payment_type = models.CharField(max_length=3, choices=[(payment, payment.value) for payment in PaymentType])
    base_cost = models.DecimalField(max_digits=3, decimal_places=2)

    amount = models.DecimalField(max_digits=3, decimal_places=2)  # Will be dynamically calculated

    @staticmethod
    def get_running_total(self):
        total = 0

        ripoffs = self.objects.all()
        for ripoff in ripoffs:
            total += ripoff.amount

        return total
