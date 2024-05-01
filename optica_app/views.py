from django.shortcuts import redirect, render
from .models import Order, Identity
from .forms import ContactForm, FrameForm, GlassTypeForm, InstitutionForm, LensForm, OrderForm, IdentityForm, PrescriptionDetailForm, ProductForm



def view_index(request):
    order = Order.objects.get(pk=1)
    identity = Identity.objects.get(order=order)
    return render(request, 'optica_app/home.html', {'order': order, 'identity': identity})

def home(request):
    return render(request, 'optica_app/index.html')


def order_view(request):
    form = OrderForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = OrderForm()

    context = {'form': form}
    return render(request, 'optica_app/form_order.html', context)


def identity_form_view(request):
    form = IdentityForm()
    if request.method == 'POST':
        form = IdentityForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('optica_app:identity')
        form = IdentityForm()

    context = {'form': form}
    return render(request, 'optica_app/form_identity.html', context)



def tunnel_form_view(request):
    order_form = OrderForm(request.POST or None)
    identity_form = IdentityForm(request.POST or None)
    contact_form = ContactForm(request.POST or None)
    institution_form = InstitutionForm(request.POST or None)
    prescription_detail_form = PrescriptionDetailForm(request.POST or None)
    product_form = ProductForm(request.POST or None)
    frame_form = FrameForm(request.POST or None)
    glass_type_form = GlassTypeForm(request.POST or None)
    lens_form = LensForm(request.POST or None)

    if all([order_form.is_valid(), identity_form.is_valid(), contact_form.is_valid(), institution_form.is_valid(), prescription_detail_form.is_valid(), product_form.is_valid(), frame_form.is_valid(), glass_type_form.is_valid(), lens_form.is_valid()]):
        order_form.save()
        identity_form.save()
        contact_form.save()
        institution_form.save()
        prescription_detail_form.save()
        product_form.save()
        frame_form.save()
        glass_type_form.save()
        lens_form.save()

        return redirect('optica_app:identity')

    context = {
        'order_form': order_form,
        'identity_form': identity_form,
        'contact_form': contact_form,
        'institution_form': institution_form,
        'prescription_detail_form': prescription_detail_form,
        'product_form': product_form,
        'frame_form': frame_form,
        'glass_type_form': glass_type_form,
        'lens_form': lens_form,
    }
    return render(request, 'optica_app/form_tunnel.html', context)
