# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com>
# project: AlexandruOpticaApp
# github: https://github.com/boot-sandre/alexandru-optica-app/
from django import forms
from django.contrib import admin
from django.template.defaultfilters import truncatechars

from .models import (
    Contact,
    Frame,
    GlassType,
    Identity,
    Institution,
    Lens,
    Order,
    PrescriptionDetail,
    Product, Voucher, VoucherLine,
)


@admin.register(PrescriptionDetail)
class PrescriptionDetailAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "fare_pupillary_distance",
        "aproape_pupillary_distance",
        "intermediar_pupillary_distance",
    )
    list_filter = ("order",)
    search_fields = (
        "order__id",
        "fare_od_spheric",
        "fare_os_spheric",
    )
    raw_id_fields = ("order",)
    fieldsets = (
        ("Order Info", {"fields": ("order",)}),
        (
            "Distance Vision",
            {
                "fields": (
                    ("fare_od_spheric", "fare_od_cylindric", "fare_od_axis"),
                    ("fare_os_spheric", "fare_os_cylindric", "fare_os_axis"),
                    "fare_pupillary_distance",
                )
            },
        ),
        (
            "Near Vision",
            {
                "fields": (
                    ("aproape_od_spheric", "aproape_od_cylindric", "aproape_od_axis"),
                    ("aproape_os_spheric", "aproape_os_cylindric", "aproape_os_axis"),
                    "aproape_pupillary_distance",
                )
            },
        ),
        (
            "Intermediate Vision",
            {
                "fields": (
                    (
                        "intermediar_od_spheric",
                        "intermediar_od_cylindric",
                        "intermediar_od_axis",
                    ),
                    (
                        "intermediar_os_spheric",
                        "intermediar_os_cylindric",
                        "intermediar_os_axis",
                    ),
                    "intermediar_pupillary_distance",
                )
            },
        ),
    )

    def get_changeform_initial_data(self, request):
        last_order = Order.objects.order_by("-id").first()
        if last_order:
            return {"order": last_order.pk}
        return {}

    def get_order_id(self, obj):
        return str(obj.order)

    get_order_id.admin_order_field = "order"
    get_order_id.short_description = "Order ID"

    def get_order_fact(self, obj):
        return obj.order.__str__()

    get_order_fact.admin_order_field = "order"
    get_order_fact.short_description = "Order Fact"


@admin.register(Identity)
class IdentityAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "order_id")
    search_fields = ("first_name", "last_name", "order__id")
    list_filter = ("order",)
    raw_id_fields = ("order",)

    def order_id(self, obj):
        return obj.order.id

    order_id.admin_order_field = "order"
    order_id.short_description = "Order ID"

    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related("order")
        return queryset

    def created(self, obj):
        return obj.order.created

    created.admin_order_field = "order__created"
    created.short_description = "Created"

    def modified(self, obj):
        return obj.order.modified

    modified.admin_order_field = "order__modified"
    modified.short_description = "Modified"


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "order_id")
    search_fields = ("phone_number",)
    raw_id_fields = ("order",)

    def get_changeform_initial_data(self, request):
        last_order = Order.objects.order_by("-id").first()
        if last_order:
            return {"order": last_order.pk}
        return {}


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ("title", "address_preview")
    search_fields = ("title", "address")
    raw_id_fields = ("order",)

    def address_preview(self, obj):
        return truncatechars(obj.address, 50)

    address_preview.short_description = "Address"

    def get_changeform_initial_data(self, request):
        last_order = Order.objects.order_by("-id").first()
        if last_order:
            return {"order": last_order.pk}
        return {}


class IdentityInline(admin.TabularInline):
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
        (
            "Distance Vision",
            {
                "fields": (
                    ("fare_od_spheric", "fare_od_cylindric", "fare_od_axis"),
                    ("fare_os_spheric", "fare_os_cylindric", "fare_os_axis"),
                    "fare_pupillary_distance",
                )
            },
        ),
        (
            "Near Vision",
            {
                "fields": (
                    ("aproape_od_spheric", "aproape_od_cylindric", "aproape_od_axis"),
                    ("aproape_os_spheric", "aproape_os_cylindric", "aproape_os_axis"),
                    "aproape_pupillary_distance",
                )
            },
        ),
        (
            "Intermediate Vision",
            {
                "fields": (
                    (
                        "intermediar_od_spheric",
                        "intermediar_od_cylindric",
                        "intermediar_od_axis",
                    ),
                    (
                        "intermediar_os_spheric",
                        "intermediar_os_cylindric",
                        "intermediar_os_axis",
                    ),
                    "intermediar_pupillary_distance",
                )
            },
        ),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("__str__", "price")


admin.site.register(Frame)
admin.site.register(GlassType)
admin.site.register(Lens)


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1


class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(OrderAdminForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["total_price"] = forms.DecimalField(
                disabled=True,
                required=False,
                decimal_places=2,
                max_digits=10,
                initial=self.instance.total_price(),
            )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm
    change_form_template = "admin/optica_app/order/change_form.html"
    fields = ["user"]
    list_display = ["__str__", "user", "created_at", "updated_at", "total_price"]

    class Meta:
        model = Order

    inlines = [
        IdentityInline,
        ContactInline,
        InstitutionInline,
        PrescriptionDetailsInline,
        ProductInline,
    ]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(OrderAdmin, self).get_readonly_fields(request, obj)
        if obj:  # cela signifie que nous sommes en mode édition
            return readonly_fields + ("total_price",)
        return readonly_fields


admin.site.register(VoucherLine)


class VoucherLineInline(admin.TabularInline):
    model = VoucherLine
    extra = 1


@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    inlines = [VoucherLineInline]
