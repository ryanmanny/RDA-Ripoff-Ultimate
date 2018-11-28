from django.db import models
from django.contrib.auth import models as auth_models

from .managers import RipoffSet
from .ripoff_calculator import RipoffCalculator

from .util import ChoicesEnum


# MODELS
class RDAPlan(models.Model):
    plans = models.Manager()

    plan = models.IntegerField(
        verbose_name="Plan Number"
    )
    base_cost = models.IntegerField(
        verbose_name="Plan Base Cost"
    )
    dollars = models.IntegerField(
        verbose_name="RDA Dollars"
    )

    class Meta:
        verbose_name = "RDA Plan"
        verbose_name_plural = "RDA Plans"

    def __str__(self):
        return f"<RDA Plan {self.plan} - ${self.dollars}"


# TODO: Investigate if this model needs to be radically unseated from the hold of inheritance from wrong thing
# Maybe AbstractBaseUser is a better parent
class SiteUser(auth_models.User):
    users = models.Manager()

    rda_plan = models.ForeignKey(
        to='RDAPlan',  # Level 0-3
        verbose_name="RDA Plan",
        related_name='users',
        on_delete=models.CASCADE,
    )
    wsu_id = models.CharField(
        verbose_name="WSU ID #",
        max_length=8,  # 11000000
    )

    def __str__(self):
        return f"<SiteUser {self.username} - RDA Plan: {self.rda_plan} - ID: {self.wsu_id}>"


class Product(models.Model):
    products = models.Manager()

    name = models.CharField(
        max_length=40,
    )

    def __str__(self):
        return f"<Product {self.name}>"


class Location(models.Model):
    locations = models.Manager()

    name = models.CharField(
        max_length=40,
    )
    discount_plan = models.ForeignKey(
        to='DiscountPlan',
        related_name='locations',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"<Location {self.name} - {self.discount_plan}>"


class DiscountPlan(models.Model):
    plans = models.Manager()

    # Percentage discounts applied to different purchase methods
    name = models.CharField(max_length=40)

    rda_discount = models.DecimalField(
        verbose_name="RDA Discount",
        max_digits=3,
        decimal_places=1,
    )
    cgr_discount = models.DecimalField(
        verbose_name="Cougar Cash Discount",
        max_digits=3,
        decimal_places=1,
    )

    def get_percent_rda_discount(self):
        return float(self.rda_discount) / 100.0

    def get_percent_cgr_discount(self):
        return float(self.cgr_discount) / 100.0

    def __str__(self):
        return f"<Discount Plan for {self.name} - RDA: {self.rda_discount} CC: {self.cgr_discount}>"


class PaymentType(ChoicesEnum):
    CRD = "Credit Card"
    CGR = "Cougar Cash"
    RDA = "RDA"


class Ripoff(models.Model):
    ripoffs = RipoffSet.as_manager()

    date = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(
        to='SiteUser',
        related_name='ripoffs',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        to='Product',
        related_name='ripoffs',
        on_delete=models.CASCADE,
    )
    location = models.ForeignKey(
        to='Location',
        related_name='ripoffs',
        on_delete=models.CASCADE,
    )

    payment_type = models.CharField(
        max_length=3,
        choices=PaymentType.as_choices(),
    )
    base_price = models.DecimalField(
        max_digits=4,
        decimal_places=2,
    )

    ripoff_amount = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        blank=True,
    )

    def calculate_ripoff_amount(self):
        return RipoffCalculator(
            payment_type=PaymentType[self.payment_type],
            base_price=self.base_price,
            discount_plan=self.location.discount_plan,
            rda_plan=self.user.rda_plan,
        ).ripoff()

    def save(self, *args, **kwargs):
        self.ripoff_amount = self.calculate_ripoff_amount()

        return super().save(*args, **kwargs)

    def __str__(self):
        return f"<Ripoff of ${self.ripoff_amount} - {self.payment_type}>"
