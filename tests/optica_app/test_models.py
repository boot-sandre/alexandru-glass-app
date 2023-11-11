import pytest
from optica_app.factory import OrderFactory, IdentityFactory, ContactFactory, InstitutionFactory, PrescriptionDetailFactory

@pytest.mark.django_db
def test_order_creation():
    order = OrderFactory()
    assert order.pk is not None, "Should create an Order instance"

@pytest.mark.django_db
def test_identity_creation():
    identity = IdentityFactory()
    assert identity.pk is not None, "Should create an Identity instance"
    assert str(identity) == f"{identity.first_name} {identity.last_name}", "Identity string representation should be first name and last name"

@pytest.mark.django_db
def test_contact_creation():
    contact = ContactFactory()
    assert contact.pk is not None, "Should create a Contact instance"
    assert len(contact.phone_number) > 0, "Contact should have a phone number"

@pytest.mark.django_db
def test_institution_creation():
    institution = InstitutionFactory()
    assert institution.pk is not None, "Should create an Institution instance"
    assert str(institution) == institution.title, "Institution string representation should be the title"


@pytest.mark.django_db
def test_prescription_detail_creation():
    prescription_detail = PrescriptionDetailFactory()

    assert prescription_detail.pk is not None, "Should create a PrescriptionDetail instance"

    # Assertions for distance vision (Fare) fields
    assert -20.00 <= prescription_detail.fare_od_spheric <= 20.00, "fare_od_spheric should be within the range -20.00 to 20.00"
    assert -20.00 <= prescription_detail.fare_od_cylindric <= 20.00, "fare_od_cylindric should be within the range -20.00 to 20.00"
    assert 0 <= prescription_detail.fare_od_axis <= 180, "fare_od_axis should be within the range 0 to 180"

    assert -20.00 <= prescription_detail.fare_os_spheric <= 20.00, "fare_os_spheric should be within the range -20.00 to 20.00"
    assert -20.00 <= prescription_detail.fare_os_cylindric <= 20.00, "fare_os_cylindric should be within the range -20.00 to 20.00"
    assert 0 <= prescription_detail.fare_os_axis <= 180, "fare_os_axis should be within the range 0 to 180"

    assert 50.0 <= prescription_detail.fare_pupillary_distance <= 70.0, "fare_pupillary_distance should be within the range 50.0 to 70.0"

    # Assertions for near vision (Aproape) fields
    assert -20.00 <= prescription_detail.aproape_od_spheric <= 20.00, "aproape_od_spheric should be within the range -20.00 to 20.00"
    assert -20.00 <= prescription_detail.aproape_od_cylindric <= 20.00, "aproape_od_cylindric should be within the range -20.00 to 20.00"
    assert 0 <= prescription_detail.aproape_od_axis <= 180, "aproape_od_axis should be within the range 0 to 180"

    assert -20.00 <= prescription_detail.aproape_os_spheric <= 20.00, "aproape_os_spheric should be within the range -20.00 to 20.00"
    assert -20.00 <= prescription_detail.aproape_os_cylindric <= 20.00, "aproape_os_cylindric should be within the range -20.00 to 20.00"
    assert 0 <= prescription_detail.aproape_os_axis <= 180, "aproape_os_axis should be within the range 0 to 180"

    assert 50.0 <= prescription_detail.aproape_pupillary_distance <= 70.0, "aproape_pupillary_distance should be within the range 50.0 to 70.0"

    # Assertions for intermediate vision (Intermediar) fields
    assert -20.00 <= prescription_detail.intermediar_od_spheric <= 20.00, "intermediar_od_spheric should be within the range -20.00 to 20.00"
    assert -20.00 <= prescription_detail.intermediar_od_cylindric <= 20.00, "intermediar_od_cylindric should be within the range -20.00 to 20.00"
    assert 0 <= prescription_detail.intermediar_od_axis <= 180, "intermediar_od_axis should be within the range 0 to 180"

    assert -20.00 <= prescription_detail.intermediar_os_spheric <= 20.00, "intermediar_os_spheric should be within the range -20.00 to 20.00"
    assert -20.00 <= prescription_detail.intermediar_os_cylindric <= 20.00, "intermediar_os_cylindric should be within the range -20.00 to 20.00"
    assert 0 <= prescription_detail.intermediar_os_axis <= 180, "intermediar_os_axis should be within the range 0 to 180"

    assert 50.0 <= prescription_detail.intermediar_pupillary_distance <= 70.0, "intermediar_pupillary_distance should be within the range 50.0 to 70.0"
