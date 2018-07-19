from django.db import models
from django.contrib.auth import models as auth_models

from RipoffServer.managers import RipoffManager

from .ripoff_logic import calculate_simple_ripoff

from enum import Enum


# MODELS
class RDAPlan(models.Model):
    plan = models.IntegerField(max_length=1, verbose_name="Plan Number")
    base_cost = models.IntegerField(max_length=4, verbose_name="Plan Base Cost")
    dollars = models.IntegerField(max_length=4, verbose_name="RDA Dollars")

    def __str__(self):
        return "<RDA Plan {NUMBER} - ${DOLLARS}".format(
            NUMBER=self.plan, DOLLARS=self.dollars)


# TODO: Investigate if this model needs to be radically unseated from the hold of inheritance from wrong thing
class SiteUser(auth_models.User):
    rda_plan = models.ForeignKey('RDAPlan', verbose_name="RDA Plan", on_delete=models.CASCADE)  # Level 0-3
    wsu_id = models.CharField(verbose_name="WSU ID Number", max_length=8)

    def __str__(self):
        return "<SiteUser {NAME} - RDA Plan: {RDA_PLAN} - ID: {ID}>".format(
            NAME=self.username, RDA_PLAN=self.rda_plan, ID=self.wsu_id)


class Product(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return "<Product {NAME}>".format(
            NAME=self.name)


class Location(models.Model):
    name = models.CharField(max_length=40)
    discount_plan = models.ForeignKey('DiscountPlan', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "<Location {NAME} - {DISCOUNT_PLAN}>".format(
            NAME=self.name, DISCOUNT_PLAN=self.discount_plan)


class DiscountPlan(models.Model):
    # Percentage discounts applied to different purchase methods
    name = models.CharField(max_length=40)

    rda_discount = models.DecimalField(verbose_name="RDA Discount", max_digits=3, decimal_places=1)
    cgr_discount = models.DecimalField(verbose_name="Cougar Cash Discount", max_digits=3, decimal_places=1)

    def __str__(self):
        return "<Discount Plan for {NAME} - RDA: {RDA_DISCOUNT} CC: {CC_DISCOUNT}>".format(
            NAME=self.name, RDA_DISCOUNT=self.rda_discount, CC_DISCOUNT=self.cc_discount)


class PaymentType(Enum):
    CRD = "Credit Card"
    CGR = "Cougar Cash"
    RDA = "RDA"


class Ripoff(models.Model):
    objects = RipoffManager()  # Supplies with create_ripoff function that dynamically calculates ripoff

    date = models.DateTimeField(auto_now=True)

    user = models.ForeignKey('SiteUser', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)

    payment_type = models.CharField(max_length=3, choices=[(payment.name, payment.value) for payment in PaymentType])
    base_price = models.DecimalField(max_digits=4, decimal_places=2)

    ripoff_amount = models.DecimalField(max_digits=4, decimal_places=2, blank=True)  # Populated by save method

    def save(self, *args, **kwargs):
        self.ripoff_amount = calculate_simple_ripoff(
            base_price=self.base_price,
            payment_type=PaymentType[self.payment_type],
            discount_plan=self.location.discount_plan,
            rda_plan=self.user.rda_plan
        )

        return super().save(*args, **kwargs)

    def __str__(self):
        return "<Ripoff of ${AMOUNT} - {PAYMENT_TYPE}>".format(
            AMOUNT=self.ripoff_amount, PAYMENT_TYPE=PaymentType[self.payment_type])
