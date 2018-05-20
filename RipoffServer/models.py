from django.db import models
from django.contrib.auth import models as auth_models

from managers import RipOffManager

from enum import Enum


class SiteUser(auth_models.User):
    rda_plan = models.IntegerField(max_length=1)  # Level 0-3


class Product(models.Model):
    name = models.CharField(max_length=40)
    # Made its own model for further extensibility later


class Location(models.Model):
    name = models.CharField(max_length=40)
    discount_plan = models.ForeignKey('DiscountPlan', on_delete=models.SET_DEFAULT)


class PaymentType(Enum):
    CRD = "Credit Card"
    CGR = "Cougar Cash"
    RDA = "RDA"


class DiscountPlan(models.Model):
    # Percentage discounts applied to different purchase methods
    rda_discount = models.FloatField(verbose_name="RDA Discount")
    cc_discount = models.FloatField(verbose_name="Cougar Cash Discount")


class RipOff(models.Model):
    objects = RipOffManager()  # Supplies with create_ripoff function that dynamically calculates ripoff

    user = models.ForeignKey('SiteUser', on_delete=models.SET_DEFAULT)
    product = models.CharField(max_length=40)
    location = models.ForeignKey('Location', on_delete=None)
    payment_type = models.CharField(max_length=3, choices=[(payment, payment.value) for payment in PaymentType])
    cost = models.DecimalField(max_digits=3, decimal_places=2)

    ripoff = models.DecimalField(max_digits=3, decimal_places=2)  # Will be dynamically calculated
