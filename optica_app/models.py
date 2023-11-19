# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com>
# project: AlexandruOpticaApp
# github: https://github.com/boot-sandre/alexandru-optica-app/
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


class Order(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="orders"
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def total_price(self) -> Decimal:
        return Decimal(self.products.aggregate(models.Sum("price"))["price__sum"] or Decimal("0.00"))

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"ODR_{self.pk:06}"


class Identity(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="identities"
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Identity"
        verbose_name_plural = "Identities"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Contact(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="contacts"
    )
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. "
        "Up to 15 digits allowed.",
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return self.phone_number


class Institution(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="institutions"
    )
    title = models.CharField(max_length=255)
    address = models.TextField()

    class Meta:
        verbose_name = "Institution"
        verbose_name_plural = "Institutions"

    def __str__(self):
        return self.title


class PrescriptionDetail(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="prescriptions"
    )
    # Validators for the optical range
    optical_range_validator = [
        MinValueValidator(Decimal("-20.00")),
        MaxValueValidator(Decimal("20.00")),
    ]
    axis_range_validator = [
        MinValueValidator(0),
        MaxValueValidator(180),
    ]
    pd_range_validator = [
        MinValueValidator(Decimal("50.0")),
        MaxValueValidator(Decimal("70.0")),
    ]

    # Fields for distance vision (Fare)
    fare_od_spheric = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=optical_range_validator,
    )
    fare_od_cylindric = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=optical_range_validator,
    )
    fare_od_axis = models.IntegerField(
        null=True,
        blank=True,
        validators=axis_range_validator,
    )

    fare_os_spheric = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=optical_range_validator,
    )
    fare_os_cylindric = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=optical_range_validator,
    )
    fare_os_axis = models.IntegerField(
        null=True,
        blank=True,
        validators=axis_range_validator,
    )

    fare_pupillary_distance = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        validators=pd_range_validator,
    )

    # Fields for near vision (Aproape)
    aproape_od_spheric = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=optical_range_validator,
    )
    aproape_od_cylindric = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=optical_range_validator,
    )
    aproape_od_axis = models.IntegerField(
        null=True,
        blank=True,
        validators=axis_range_validator,
    )

    aproape_os_spheric = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=optical_range_validator,
    )
    aproape_os_cylindric = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=optical_range_validator,
    )
    aproape_os_axis = models.IntegerField(
        null=True,
        blank=True,
        validators=axis_range_validator,
    )

    aproape_pupillary_distance = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        validators=pd_range_validator,
    )

    # Fields for intermediate vision (Intermediar)
    intermediar_od_spheric = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=optical_range_validator,
    )
    intermediar_od_cylindric = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=optical_range_validator,
    )
    intermediar_od_axis = models.IntegerField(
        null=True,
        blank=True,
        validators=axis_range_validator,
    )

    intermediar_os_spheric = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=optical_range_validator,
    )
    intermediar_os_cylindric = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=optical_range_validator,
    )
    intermediar_os_axis = models.IntegerField(
        null=True,
        blank=True,
        validators=axis_range_validator,
    )

    intermediar_pupillary_distance = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        validators=pd_range_validator,
    )

    class Meta:
        verbose_name = "Prescription Detail"
        verbose_name_plural = "Prescription Details"

    def __str__(self):
        return f"Prescription for Order {self.order.pk}"


class Product(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="products")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)]
    )
    frame = models.ForeignKey(
        "Frame", on_delete=models.PROTECT, related_name="product_set"
    )
    glass_type = models.ForeignKey(
        "GlassType", on_delete=models.PROTECT, related_name="product_set"
    )
    lens = models.ForeignKey(
        "Lens", on_delete=models.PROTECT, related_name="product_set"
    )

    def __str__(self):
        return f"{self.frame} - {self.glass_type} - {self.lens}"


class Frame(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class GlassType(models.Model):
    DISTANCE_CHOICES = [
        ("FAR", "Far"),
        ("MEDIUM", "Medium"),
        ("NEAR", "Near"),
    ]
    TREATMENT_CHOICES = [
        ("POLARIZED", "Polarized"),
        ("UV_PROTECTION", "UV Protection"),
        ("ANTI_REFLECTIVE", "Anti-Reflective"),
    ]

    distance = models.CharField(
        max_length=100,
        choices=DISTANCE_CHOICES,
        default="NEAR",
        verbose_name="Distance",
    )
    treatment = models.CharField(
        max_length=100,
        choices=TREATMENT_CHOICES,
        verbose_name="Tratament",
        blank=True,
        null=True,
    )

    def __str__(self):
        distance_display = self.get_distance_display()
        treatment_display = (
            f", {self.get_treatment_display()}" if self.treatment else ""
        )
        return f"{distance_display}{treatment_display}"


class Lens(models.Model):
    title = models.TextField()

    def __str__(self):
        return self.title


class Voucher(models.Model):
    PAYMENT_CHOICES = [
        ("CASH", "Cash"),
        ("CARD", "Card"),
        ("IGC", "ItsGetComplicated"),
    ]
    orders = models.ManyToManyField(Order, related_name="vouchers")
    payment_method = models.TextField("Payment Method", choices=PAYMENT_CHOICES)

    def orders_total_price(self) -> Decimal:
        return Decimal(self.orders.aggregate(models.Sum("products__price"))["products__price__sum"] or Decimal("0.00"))

    def voucher_lines_total_amount(self) -> Decimal:
        return Decimal(self.voucher_lines.aggregate(models.Sum("amount"))["amount__sum"] or Decimal("0.00"))

    def rest_amount(self) -> Decimal:
        return Decimal(self.orders_total_price() - self.voucher_lines_total_amount())


class VoucherLine(models.Model):
    voucher = models.ForeignKey(Voucher, on_delete=models.PROTECT, related_name="voucher_lines")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_ref = models.CharField(max_length=250, blank=True, null=True)
