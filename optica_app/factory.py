# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com>
# project: AlexandruOpticaApp
# github: https://github.com/boot-sandre/alexandru-optica-app/
import factory
from factory import fuzzy

from .models import Contact, Identity, Institution, Order, PrescriptionDetail, Lens, GlassType, Frame, Product

# factories.py
import factory
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = make_password('password')
    is_superuser = True
    is_staff = True


class OrderFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory('optica_app.factory.UserFactory')

    class Meta:
        model = Order


class IdentityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Identity

    order = factory.SubFactory(OrderFactory)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")


class ContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contact

    order = factory.SubFactory(OrderFactory)
    phone_number = factory.Faker("phone_number")


class InstitutionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Institution

    order = factory.SubFactory(OrderFactory)
    title = factory.Faker("company")
    address = factory.Faker("address")


class PrescriptionDetailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PrescriptionDetail

    order = factory.SubFactory(OrderFactory)

    # Fields for distance vision (Fare)
    fare_od_spheric = fuzzy.FuzzyDecimal(-20.00, 20.00, 2)
    fare_od_cylindric = fuzzy.FuzzyDecimal(-20.00, 20.00, 2)
    fare_od_axis = fuzzy.FuzzyInteger(0, 180)

    fare_os_spheric = fuzzy.FuzzyDecimal(-20.00, 20.00, 2)
    fare_os_cylindric = fuzzy.FuzzyDecimal(-20.00, 20.00, 2)
    fare_os_axis = fuzzy.FuzzyInteger(0, 180)

    fare_pupillary_distance = fuzzy.FuzzyDecimal(50.0, 70.0, 1)

    # Fields for near vision (Aproape)
    aproape_od_spheric = fuzzy.FuzzyDecimal(-20.00, 20.00, 2)
    aproape_od_cylindric = fuzzy.FuzzyDecimal(-20.00, 20.00, 2)
    aproape_od_axis = fuzzy.FuzzyInteger(0, 180)

    aproape_os_spheric = fuzzy.FuzzyDecimal(-20.00, 20.00, 2)
    aproape_os_cylindric = fuzzy.FuzzyDecimal(-20.00, 20.00, 2)
    aproape_os_axis = fuzzy.FuzzyInteger(0, 180)

    aproape_pupillary_distance = fuzzy.FuzzyDecimal(50.0, 70.0, 1)

    # Fields for intermediate vision (Intermediar)
    intermediar_od_spheric = fuzzy.FuzzyDecimal(-20.00, 20.00, 2)
    intermediar_od_cylindric = fuzzy.FuzzyDecimal(-20.00, 20.00, 2)
    intermediar_od_axis = fuzzy.FuzzyInteger(0, 180)

    intermediar_os_spheric = fuzzy.FuzzyDecimal(-20.00, 20.00, 2)
    intermediar_os_cylindric = fuzzy.FuzzyDecimal(-20.00, 20.00, 2)
    intermediar_os_axis = fuzzy.FuzzyInteger(0, 180)

    intermediar_pupillary_distance = fuzzy.FuzzyDecimal(50.0, 70.0, 1)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    order = factory.SubFactory(OrderFactory)
    total_price = fuzzy.FuzzyDecimal(0.01, 1000.00, 2)

    @factory.post_generation
    def post_create(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        # Assuming that each Product should have one Frame, one GlassType, and one Lens
        Frame.objects.create(product=self, title=f"Frame for product {self.pk}")
        GlassType.objects.create(
            product=self,
            distance=fuzzy.FuzzyChoice([choice[0] for choice in GlassType.DISTANCE_CHOICES]).fuzz(),
            treatment=fuzzy.FuzzyChoice([choice[0] for choice in GlassType.TREATMENT_CHOICES]).fuzz()
        )
        Lens.objects.create(product=self, title=f"Lens for product {self.pk}")


class FrameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Frame

    product = factory.SubFactory(ProductFactory)
    title = factory.Sequence(lambda n: f"Frame Title {n}")


class GlassTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GlassType

    product = factory.SubFactory(ProductFactory)
    distance = fuzzy.FuzzyChoice(choices=[choice[0] for choice in GlassType.DISTANCE_CHOICES])
    treatment = fuzzy.FuzzyChoice(choices=[choice[0] for choice in GlassType.TREATMENT_CHOICES], getter=lambda c: c if c is not None else '')


class LensFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Lens

    product = factory.SubFactory(ProductFactory)
    title = factory.Faker('text', max_nb_chars=200)