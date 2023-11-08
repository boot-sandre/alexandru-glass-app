# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com>
# project: AlexandruGlassApp
# github: https://github.com/boot-sandre/alexandru-glass-app/
from django.core.validators import RegexValidator
from django.db import models


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"ODR_{self.pk:06}"


class Identity(models.Model):
    """ Order metadata"""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='identities')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Identity"
        verbose_name_plural = "Identities"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Contact(models.Model):
    """ Order metadata"""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='contacts')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return self.phone_number


class Institution(models.Model):
    """ Order metadata"""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='institutions')
    title = models.CharField(max_length=255)
    address = models.TextField()

    class Meta:
        verbose_name = "Institution"
        verbose_name_plural = "Institutions"

    def __str__(self):
        return self.title


class PrescriptionDetail(models.Model):
    """ Order metadata"""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='prescriptions')

    # Fields for distance vision (Fare)
    fare_od_spheric = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fare_od_cylindric = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fare_od_axis = models.IntegerField(null=True, blank=True)

    fare_os_spheric = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fare_os_cylindric = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fare_os_axis = models.IntegerField(null=True, blank=True)

    fare_pupillary_distance = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)

    # Fields for near vision (Aproape)
    aproape_od_spheric = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    aproape_od_cylindric = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    aproape_od_axis = models.IntegerField(null=True, blank=True)

    aproape_os_spheric = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    aproape_os_cylindric = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    aproape_os_axis = models.IntegerField(null=True, blank=True)

    aproape_pupillary_distance = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)

    # Fields for intermediate vision (Intermediar)
    intermediar_od_spheric = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    intermediar_od_cylindric = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    intermediar_od_axis = models.IntegerField(null=True, blank=True)

    intermediar_os_spheric = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    intermediar_os_cylindric = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    intermediar_os_axis = models.IntegerField(null=True, blank=True)

    intermediar_pupillary_distance = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)

    class Meta:
        verbose_name = "Prescription Detail"
        verbose_name_plural = "Prescription Details"

    def __str__(self):
        return f"Prescription for Order {self.order.pk}"


class Product(models.Model):
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.frame.title} - {self.total_price}"


class Frame(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class GlassType(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    distance = models.CharField(max_length=100)
    near = models.CharField(max_length=100)
    other = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.distance}, {self.near}, {self.other}"


class Lens(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    title = models.TextField()

    def __str__(self):
        return self.title

