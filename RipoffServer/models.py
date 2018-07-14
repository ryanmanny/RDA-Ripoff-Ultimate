from django.db import models
from django.contrib.auth import models as auth_models

from RipoffServer.managers import RipoffManager

from enum import Enum


# MODELS
class SiteUser(auth_models.User):
    rda_plan = models.IntegerField(verbose_name="RDA Plan")  # Level 0-3
    wsu_id = models.CharField(verbose_name="WSU ID Number", max_length=8)

    def __str__(self):
        return "<" + str(self.username) + " - " + str(self.wsu_id) + ">"


class Product(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return "<" + str(self.name) + ">"


class Location(models.Model):
    name = models.CharField(max_length=40)
    discount_plan = models.ForeignKey('DiscountPlan', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "<" + str(self.name) + " - " + str(self.discount_plan) + ">"


class DiscountPlan(models.Model):
    # Percentage discounts applied to different purchase methods
    name = models.CharField(max_length=40)

    rda_discount = models.DecimalField(verbose_name="RDA Discount", max_digits=3, decimal_places=1)
    cc_discount = models.DecimalField(verbose_name="Cougar Cash Discount", max_digits=3, decimal_places=1)

    def __str__(self):
        return "<" + "RDA: " + str(self.rda_discount) + ", CC: " + str(self.cc_discount) + ">"


class PaymentType(Enum):
    CRD = "Credit Card"
    CGR = "Cougar Cash"
    RDA = "RDA"


class Ripoff(models.Model):
    objects = RipoffManager()  # Supplies with create_ripoff function that dynamically calculates ripoff

    date = models.DateTimeField(auto_now=True)

    user = models.ForeignKey('SiteUser', null=True, on_delete=models.SET_NULL)
    product = models.CharField(max_length=40)
    location = models.ForeignKey('Location', on_delete=None)
    payment_type = models.CharField(max_length=3, choices=[(payment, payment.value) for payment in PaymentType])
    base_cost = models.DecimalField(max_digits=3, decimal_places=2)

    ripoff_amount = models.DecimalField(max_digits=3, decimal_places=2, blank=True)  # Will be dynamically calculated

    @staticmethod
    def calculate_simple_ripoff(base_cost, payment_type, discount_plan):
        # TODO: Implement
        return base_cost

    def save(self, *args, **kwargs):
        ripoff = self.calculate_simple_ripoff(**kwargs)

        return super().save(*args, **kwargs)

    def __str__(self):
        return "<" + "$" + str(self.ripoff_amount) + " - " + str(self.payment_type) + ">"
