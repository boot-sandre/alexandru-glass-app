from django import forms
from .models import Identity, Contact, Institution, Order, PrescriptionDetail, Product, Frame, GlassType, Lens, Voucher, VoucherLine


class IdentityForm(forms.ModelForm):
    class Meta:
        model = Identity
        fields = '__all__'

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = '__all__'

class PrescriptionDetailForm(forms.ModelForm):
    class Meta:
        model = PrescriptionDetail
        fields = '__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class FrameForm(forms.ModelForm):
    class Meta:
        model = Frame
        fields = '__all__'

class GlassTypeForm(forms.ModelForm):
    class Meta:
        model = GlassType
        fields = '__all__'

class LensForm(forms.ModelForm):
    class Meta:
        model = Lens
        fields = '__all__'

class VoucherForm(forms.ModelForm):
    class Meta:
        model = Voucher
        fields = '__all__'

class VoucherLineForm(forms.ModelForm):
    class Meta:
        model = VoucherLine
        fields = '__all__'

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class TunnelForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'