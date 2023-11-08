from django.contrib import admin
from django.template.defaultfilters import truncatechars
from django.urls import reverse
from django.utils.html import format_html

from .models import Order, PrescriptionDetail, Identity, Contact, Institution, GlassType, Lens, Product, Frame

"""
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_at', 'updated_at')  # Replace 'other_field' with other relevant fields of the Order model
    search_fields = ('id',)  # Allow searching by order ID
"""


@admin.register(PrescriptionDetail)
class PrescriptionDetailAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'fare_pupillary_distance', 'aproape_pupillary_distance', 'intermediar_pupillary_distance')
    list_filter = ('order',)  # Allows filtering by the related order
    search_fields = ('order__id', 'fare_od_spheric', 'fare_os_spheric')  # Allows searching by related order ID and spheric values
    raw_id_fields = ('order',)  # Helpful if there are many orders to choose from
    fieldsets = (
        ("Order Info", {'fields': ('order',)}),
        ('Distance Vision', {
            'fields': (('fare_od_spheric', 'fare_od_cylindric', 'fare_od_axis'),
                       ('fare_os_spheric', 'fare_os_cylindric', 'fare_os_axis'),
                       'fare_pupillary_distance')
        }),
        ('Near Vision', {
            'fields': (('aproape_od_spheric', 'aproape_od_cylindric', 'aproape_od_axis'),
                       ('aproape_os_spheric', 'aproape_os_cylindric', 'aproape_os_axis'),
                       'aproape_pupillary_distance')
        }),
        ('Intermediate Vision', {
            'fields': (('intermediar_od_spheric', 'intermediar_od_cylindric', 'intermediar_od_axis'),
                       ('intermediar_os_spheric', 'intermediar_os_cylindric', 'intermediar_os_axis'),
                       'intermediar_pupillary_distance')
        }),
    )


    def get_changeform_initial_data(self, request):
        # Set the initial value for the 'order' field to the most recent Order
        last_order = Order.objects.order_by('-id').first()
        if last_order:
            return {'order': last_order.pk}
        return {}
    def get_order_id(self, obj):
        return str(obj.order)
    get_order_id.admin_order_field = 'order'
    get_order_id.short_description = 'Order ID'

    def get_order_fact(self, obj):
        return obj.order.__str__()
    get_order_fact.admin_order_field = 'order'
    get_order_fact.short_description = 'Order Fact'


@admin.register(Identity)
class IdentityAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'order_id')
    search_fields = ('first_name', 'last_name', 'order__id')
    list_filter = ('order',)
    raw_id_fields = ('order',)

    def order_id(self, obj):
        return obj.order.id
    order_id.admin_order_field = 'order'
    order_id.short_description = 'Order ID'

    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related('order')
        return queryset

    def created(self, obj):
        return obj.order.created
    created.admin_order_field = 'order__created'  # Allows sorting by the 'created' timestamp
    created.short_description = 'Created'

    def modified(self, obj):
        return obj.order.modified
    modified.admin_order_field = 'order__modified'  # Allows sorting by the 'modified' timestamp
    modified.short_description = 'Modified'


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'order_id')
    search_fields = ('phone_number',)
    raw_id_fields = ('order',)

    def get_changeform_initial_data(self, request):
        # Set the initial value for the 'order' field to the most recent Order
        last_order = Order.objects.order_by('-id').first()
        if last_order:
            return {'order': last_order.pk}
        return {}



@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('title', 'address_preview')
    search_fields = ('title', 'address')
    raw_id_fields = ('order',)

    def address_preview(self, obj):
        return truncatechars(obj.address, 50)  # Show up to 50 characters of the address
    address_preview.short_description = 'Address'

    def get_changeform_initial_data(self, request):
        # Set the initial value for the 'order' field to the most recent Order
        last_order = Order.objects.order_by('-id').first()
        if last_order:
            return {'order': last_order.pk}
        return {}


class IdentityInline(admin.TabularInline):  # or admin.StackedInline for a different layout
    model = Identity
    extra = 1


class ContactInline(admin.StackedInline):
    model = Contact
    extra = 0


class InstitutionInline(admin.TabularInline):
    model = Institution
    extra = 0


class PrescriptionDetailsInline(admin.StackedInline):
    model = PrescriptionDetail
    extra = 0
    fieldsets = (
        ('Distance Vision', {
            'fields': (('fare_od_spheric', 'fare_od_cylindric', 'fare_od_axis'),
                       ('fare_os_spheric', 'fare_os_cylindric', 'fare_os_axis'),
                       'fare_pupillary_distance')
        }),
        ('Near Vision', {
            'fields': (('aproape_od_spheric', 'aproape_od_cylindric', 'aproape_od_axis'),
                       ('aproape_os_spheric', 'aproape_os_cylindric', 'aproape_os_axis'),
                       'aproape_pupillary_distance')
        }),
        ('Intermediate Vision', {
            'fields': (('intermediar_od_spheric', 'intermediar_od_cylindric', 'intermediar_od_axis'),
                       ('intermediar_os_spheric', 'intermediar_os_cylindric', 'intermediar_os_axis'),
                       'intermediar_pupillary_distance')
        }),
    )


# Add other inlines for your submodels here
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        IdentityInline,
        ContactInline,
        InstitutionInline,
        PrescriptionDetailsInline,
        # Add other inlines here
    ]


class FrameInline(admin.StackedInline):
    model = Frame
    can_delete = False


class GlassTypeInline(admin.StackedInline):
    model = GlassType
    can_delete = False


class LensInline(admin.StackedInline):
    model = Lens
    can_delete = False


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        FrameInline,
        GlassTypeInline,
        LensInline,
    ]
    list_display = ('__str__', 'total_price')


admin.site.register(Product, ProductAdmin)
