from django.db import models
from django.contrib.auth import models as auth_models

from .managers import SiteUserManager
from .managers import LocationManager, LocationSet
from .managers import RipoffManager, RipoffSet

from .util import ChoicesEnum


# MODELS
class RDAPlan(models.Model):
    # TODO: Find a way to sensibly add dollars to an RDA Plan (HARD!)
    plans = models.Manager()

    plan = models.IntegerField(
        verbose_name="Plan Number",
        unique=True,
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

    def real_cost(self, cost):
        """Adds virtual portion of base cost spent to item cost
        """
        try:
            return cost + self.base_cost * (cost / self.dollars)
        except ZeroDivisionError:  # Plan has no dollars, cost impossible
            return float("inf")

    def __str__(self):
        return f"<RDA Plan {self.plan} - ${self.dollars}"


class SiteUser(auth_models.AbstractUser):
    users = SiteUserManager()

    rda_plan = models.ForeignKey(
        to='RDAPlan',  # Level 0-3
        verbose_name="RDA Plan",
        related_name='users',
        default=RDAPlan.plans.get(plan=0),  # Default to Plan 0
        on_delete=models.SET_DEFAULT,
    )
    wsu_id = models.CharField(
        verbose_name="WSU ID #",
        max_length=8,  # 11000000
    )

    def __str__(self):
        return f"<SiteUser {self.email} - RDA Plan: {self.rda_plan} - ID: {self.wsu_id}>"


class Product(models.Model):
    products = models.Manager()

    name = models.CharField(
        max_length=40,
    )

    def __str__(self):
        return f"<Product {self.name}>"


class Location(models.Model):
    locations = LocationManager.from_queryset(LocationSet)()

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

    @property
    def rda_discount_percent(self):
        return self.rda_discount / 100

    @property
    def cgr_discount_percent(self):
        return self.cgr_discount / 100

    def __str__(self):
        return f"<Discount Plan for {self.name} - RDA: {self.rda_discount} CC: {self.cgr_discount}>"


class PaymentType(ChoicesEnum):
    CRD = "Credit Card"
    CGR = "Cougar Cash"
    RDA = "RDA"


class Ripoff(models.Model):
    ripoffs = RipoffManager.from_queryset(RipoffSet)

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
        from .ripoff_calculator import RipoffCalculator

        return RipoffCalculator(
            user=self.user,
            payment_type=PaymentType[self.payment_type],
            base_price=self.base_price,
            location=self.location,
        ).ripoff()

    def save(self, *args, **kwargs):
        self.ripoff_amount = self.calculate_ripoff_amount()

        return super().save(*args, **kwargs)

    def __str__(self):
        return f"<Ripoff of ${self.ripoff_amount} - {self.payment_type}>"
