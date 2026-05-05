from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django import forms
from django.contrib.auth.hashers import check_password
from functools import wraps

from .models import *
from .forms import *


# =============================================================================
# ADMIN AUTHENTICATION
# =============================================================================

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')

        messages.error(request, 'Invalid username or password')

    return render(request, 'adminpanel/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# =============================================================================
# ADMIN DASHBOARD
# =============================================================================

@login_required
def dashboard(request):
    # Seed default services if not already present
    Service.seed_default_services()

    status_data = Order.objects.values('order_status').annotate(total=Count('id'))
    status_labels = [item['order_status'] for item in status_data]
    status_values = [item['total'] for item in status_data]

    context = {
        'customer_count':    Customer.objects.count(),
        'order_count':       Order.objects.count(),
        'service_count':     Service.objects.count(),
        'enquiry_count':     ContactEnquiry.objects.filter(enquiry_status='New').count(),

        'total_sales':       Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0,

        'pending_orders':    Order.objects.filter(order_status='Pending').count(),
        'stitching_orders':  Order.objects.filter(order_status='Stitching').count(),
        'ready_orders':      Order.objects.filter(order_status='Ready').count(),
        'delivered_orders':  Order.objects.filter(order_status='Delivered').count(),
        'cancelled_orders':  Order.objects.filter(order_status='Cancelled').count(),

        'paid_orders':       Order.objects.filter(payment_status='Paid').count(),
        'partial_orders':    Order.objects.filter(payment_status='Partially Paid').count(),
        'unpaid_orders':     Order.objects.filter(payment_status='Unpaid').count(),

        'recent_orders':     Order.objects.select_related('customer').order_by('-created_at')[:6],
        'recent_enquiries':  ContactEnquiry.objects.order_by('-created_at')[:5],

        'status_labels':     status_labels,
        'status_values':     status_values,
    }

    return render(request, 'adminpanel/dashboard.html', context)


# =============================================================================
# COMMON SEARCH / LIST HELPER
# =============================================================================

def crud_list(request, model, template, context_name):
    q = request.GET.get('q', '')
    objects = model.objects.all().order_by('-id')

    if q:
        if model == Customer:
            objects = objects.filter(
                Q(full_name__icontains=q) | Q(phone__icontains=q)
            )
        elif model == Service:
            objects = objects.filter(
                Q(service_name__icontains=q) | Q(gender_type__icontains=q)
            )
        elif model == Order:
            objects = objects.filter(
                Q(order_no__icontains=q) | Q(customer__full_name__icontains=q)
            )
        elif model == ContactEnquiry:
            objects = objects.filter(
                Q(name__icontains=q) | Q(phone__icontains=q) | Q(email__icontains=q)
            )

    return render(request, template, {context_name: objects, 'q': q})


# =============================================================================
# ADMIN — CUSTOMER CRUD
# =============================================================================

@login_required
def customer_list(request):
    return crud_list(request, Customer, 'adminpanel/customer_list.html', 'customers')


@login_required
def customer_form(request, pk=None):
    obj = get_object_or_404(Customer, pk=pk) if pk else None
    form = CustomerForm(request.POST or None, instance=obj)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Customer saved successfully')
        return redirect('customers')

    return render(request, 'adminpanel/form.html', {'form': form, 'title': 'Customer'})


@login_required
@require_POST
def customer_delete(request, pk):
    get_object_or_404(Customer, pk=pk).delete()
    messages.success(request, 'Customer deleted')
    return redirect('customers')


# =============================================================================
# ADMIN — SERVICE CRUD
# =============================================================================

@login_required
def service_list(request):
    Service.seed_default_services()
    return crud_list(request, Service, 'adminpanel/service_list.html', 'services')


@login_required
def service_form(request, pk=None):
    obj = get_object_or_404(Service, pk=pk) if pk else None
    form = ServiceForm(request.POST or None, instance=obj)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Service saved successfully')
        return redirect('services')

    return render(request, 'adminpanel/form.html', {'form': form, 'title': 'Service'})


@login_required
@require_POST
def service_delete(request, pk):
    get_object_or_404(Service, pk=pk).delete()
    messages.success(request, 'Service deleted')
    return redirect('services')


# =============================================================================
# ADMIN — SERVICE PRICE CRUD
# =============================================================================

@login_required
def price_list(request):
    prices = ServicePrice.objects.select_related('service').order_by('-id')
    return render(request, 'adminpanel/price_list.html', {'prices': prices})


@login_required
def price_form(request, pk=None):
    obj = get_object_or_404(ServicePrice, pk=pk) if pk else None
    form = ServicePriceForm(request.POST or None, instance=obj)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Price saved successfully')
        return redirect('prices')

    return render(request, 'adminpanel/form.html', {'form': form, 'title': 'Price'})


@login_required
@require_POST
def price_delete(request, pk):
    get_object_or_404(ServicePrice, pk=pk).delete()
    messages.success(request, 'Price deleted')
    return redirect('prices')


# =============================================================================
# ADMIN — ORDER CRUD
# =============================================================================

@login_required
def order_list(request):
    orders = Order.objects.select_related('customer').order_by('-id')
    return render(request, 'adminpanel/order_list.html', {'orders': orders})


@login_required
def order_form(request, pk=None):
    obj = get_object_or_404(Order, pk=pk) if pk else None
    form = OrderForm(request.POST or None, instance=obj)

    if request.method == 'POST' and form.is_valid():
        order = form.save(commit=False)
        if not obj:
            order.created_by = request.user
        order.save()
        messages.success(request, 'Order saved successfully')
        return redirect('orders')

    return render(request, 'adminpanel/form.html', {'form': form, 'title': 'Order'})


@login_required
@require_POST
def order_delete(request, pk):
    get_object_or_404(Order, pk=pk).delete()
    messages.success(request, 'Order deleted')
    return redirect('orders')


@login_required
def order_item_form(request):
    form = OrderItemForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Order item added')
        return redirect('orders')

    return render(request, 'adminpanel/form.html', {'form': form, 'title': 'Order Item'})


@login_required
def payment_form(request):
    form = PaymentForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Payment added')
        return redirect('orders')

    return render(request, 'adminpanel/form.html', {'form': form, 'title': 'Payment'})


# =============================================================================
# ADMIN — MEASUREMENTS
# =============================================================================

@login_required
def measurement_list(request):
    men    = MenMeasurement.objects.select_related('customer').order_by('-id')
    ladies = LadiesMeasurement.objects.select_related('customer').order_by('-id')

    return render(request, 'adminpanel/measurement_list.html', {
        'men': men,
        'ladies': ladies,
    })


@login_required
def men_measurement_form(request, pk=None):
    obj  = get_object_or_404(MenMeasurement, pk=pk) if pk else None
    form = MenMeasurementForm(request.POST or None, request.FILES or None, instance=obj)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Men measurement saved')
        return redirect('measurements')

    return render(request, 'adminpanel/form.html', {'form': form, 'title': 'Men Measurement'})


@login_required
def ladies_measurement_form(request, pk=None):
    obj  = get_object_or_404(LadiesMeasurement, pk=pk) if pk else None
    form = LadiesMeasurementForm(request.POST or None, request.FILES or None, instance=obj)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Ladies measurement saved')
        return redirect('measurements')

    return render(request, 'adminpanel/form.html', {'form': form, 'title': 'Ladies Measurement'})


# =============================================================================
# ADMIN — GALLERY
# =============================================================================

@login_required
def gallery_list(request):
    gallery = Gallery.objects.order_by('-id')
    return render(request, 'adminpanel/gallery_list.html', {'gallery': gallery})


@login_required
def gallery_form(request, pk=None):
    obj  = get_object_or_404(Gallery, pk=pk) if pk else None
    form = GalleryForm(request.POST or None, request.FILES or None, instance=obj)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Gallery saved')
        return redirect('gallery')

    return render(request, 'adminpanel/form.html', {'form': form, 'title': 'Gallery'})


@login_required
@require_POST
def gallery_delete(request, pk):
    get_object_or_404(Gallery, pk=pk).delete()
    messages.success(request, 'Gallery deleted')
    return redirect('gallery')


# =============================================================================
# ADMIN — ENQUIRIES
# =============================================================================

@login_required
def enquiry_list(request):
    enquiries = ContactEnquiry.objects.order_by('-id')
    return render(request, 'adminpanel/enquiry_list.html', {'enquiries': enquiries})


@login_required
def enquiry_form(request, pk):
    obj  = get_object_or_404(ContactEnquiry, pk=pk)
    form = ContactEnquiryForm(request.POST or None, instance=obj)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Enquiry updated')
        return redirect('enquiries')

    return render(request, 'adminpanel/form.html', {'form': form, 'title': 'Contact Enquiry'})


# =============================================================================
# ADMIN — REPORTS
# =============================================================================

@login_required
def reports(request):
    context = {
        'orders_by_status': Order.objects.values('order_status').annotate(total=Count('id')),
        'payments_total':   Payment.objects.aggregate(total=Sum('amount'))['total'] or 0,
        'sales_total':      Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0,
        'customer_total':   Customer.objects.count(),
        'service_total':    Service.objects.count(),
    }

    return render(request, 'adminpanel/reports.html', context)


# =============================================================================
# ADMIN — SITE SETTINGS
# =============================================================================

@login_required
def settings_form(request):
    obj  = SiteSetting.objects.first()
    form = SiteSettingForm(request.POST or None, request.FILES or None, instance=obj)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Settings saved')
        return redirect('settings')

    return render(request, 'adminpanel/form.html', {'form': form, 'title': 'Site Settings'})


# =============================================================================
# CUSTOMER WEBSITE — AUTH DECORATOR
# =============================================================================

def customer_required(view_func):
    """Session-based login guard for customer-facing pages."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('customer_id'):
            messages.error(request, 'Please login first')
            return redirect('customer_login')
        return view_func(request, *args, **kwargs)
    return wrapper


# =============================================================================
# CUSTOMER WEBSITE — PUBLIC PAGES
# =============================================================================

def customer_home(request):
    Service.seed_default_services()

    services = Service.objects.filter(is_active=True).order_by('id')[:6]
    gallery  = Gallery.objects.filter(is_active=True).order_by('-id')[:6]

    return render(request, 'customer/home.html', {
        'services': services,
        'gallery':  gallery,
    })


def customer_services(request):
    Service.seed_default_services()

    q        = request.GET.get('q', '')
    services = Service.objects.filter(is_active=True).order_by('id')

    if q:
        services = services.filter(
            Q(service_name__icontains=q) | Q(gender_type__icontains=q)
        )

    return render(request, 'customer/services.html', {'services': services, 'q': q})


def customer_gallery(request):
    gallery = Gallery.objects.filter(is_active=True).order_by('-id')
    return render(request, 'customer/gallery.html', {'gallery': gallery})


def customer_contact(request):
    if request.method == 'POST':
        ContactEnquiry.objects.create(
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message'),
        )
        messages.success(request, 'Your enquiry has been submitted')
        return redirect('customer_contact')

    return render(request, 'customer/contact.html')


# =============================================================================
# CUSTOMER WEBSITE — REGISTRATION & LOGIN
# =============================================================================

def customer_register(request):
    form = CustomerRegisterForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        phone = form.cleaned_data['phone']

        if Customer.objects.filter(phone=phone).exists():
            messages.error(request, 'Phone number already registered')
        else:
            form.save()
            messages.success(request, 'Registration successful. Please login.')
            return redirect('customer_login')

    return render(request, 'customer/register.html', {'form': form})


def customer_login(request):
    form = CustomerLoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        phone    = form.cleaned_data['phone']
        password = form.cleaned_data['password']

        customer = Customer.objects.filter(phone=phone, is_active=True).first()

        if customer and customer.password and check_password(password, customer.password):
            request.session['customer_id']   = customer.id
            request.session['customer_name'] = customer.full_name
            return redirect('customer_dashboard')

        messages.error(request, 'Invalid phone or password')

    return render(request, 'customer/login.html', {'form': form})


def customer_logout(request):
    request.session.flush()
    return redirect('customer_home')


# =============================================================================
# CUSTOMER WEBSITE — PROTECTED PAGES
# =============================================================================

@customer_required
def customer_dashboard(request):
    customer = get_object_or_404(Customer, id=request.session['customer_id'])
    orders   = Order.objects.filter(customer=customer).order_by('-id')[:5]

    return render(request, 'customer/dashboard.html', {
        'customer': customer,
        'orders':   orders,
    })


@customer_required
def customer_profile(request):
    customer = get_object_or_404(Customer, id=request.session['customer_id'])
    form     = CustomerRegisterForm(request.POST or None, instance=customer)

    if request.method == 'POST' and form.is_valid():
        form.save()
        request.session['customer_name'] = customer.full_name
        messages.success(request, 'Profile updated successfully')
        return redirect('customer_profile')

    return render(request, 'customer/profile.html', {'form': form})


@customer_required
def customer_my_orders(request):
    customer = get_object_or_404(Customer, id=request.session['customer_id'])
    orders   = Order.objects.filter(customer=customer).order_by('-id')

    return render(request, 'customer/my_orders.html', {'orders': orders})


@customer_required
def customer_order_detail(request, pk):
    customer = get_object_or_404(Customer, id=request.session['customer_id'])
    order    = get_object_or_404(
        Order.objects.select_related('customer'),
        id=pk,
        customer=customer,
    )
    items    = order.items.select_related('service').all()
    payments = Payment.objects.filter(order=order).order_by('-id')

    return render(request, 'customer/order_detail.html', {
        'order':    order,
        'items':    items,
        'payments': payments,
    })


# =============================================================================
# CUSTOMER WEBSITE — MEASUREMENTS
# =============================================================================

@customer_required
def customer_measurements(request):
    customer = get_object_or_404(Customer, id=request.session['customer_id'])
    men      = MenMeasurement.objects.filter(customer=customer).order_by('-id')
    ladies   = LadiesMeasurement.objects.filter(customer=customer).order_by('-id')

    return render(request, 'customer/measurements.html', {
        'customer': customer,
        'men':      men,
        'ladies':   ladies,
    })


@customer_required
def customer_men_measurement_add(request):
    customer = get_object_or_404(Customer, id=request.session['customer_id'])
    form     = MenMeasurementForm(
        request.POST or None,
        request.FILES or None,
        initial={'customer': customer},
    )
    form.fields['customer'].widget = forms.HiddenInput()

    if request.method == 'POST' and form.is_valid():
        measurement          = form.save(commit=False)
        measurement.customer = customer
        measurement.save()
        messages.success(request, 'Men measurement saved')
        return redirect('customer_measurements')

    return render(request, 'customer/form.html', {
        'form':  form,
        'title': 'Add Men Measurement',
    })


@customer_required
def customer_ladies_measurement_add(request):
    customer = get_object_or_404(Customer, id=request.session['customer_id'])
    form     = LadiesMeasurementForm(
        request.POST or None,
        request.FILES or None,
        initial={'customer': customer},
    )
    form.fields['customer'].widget = forms.HiddenInput()

    if request.method == 'POST' and form.is_valid():
        measurement          = form.save(commit=False)
        measurement.customer = customer
        measurement.save()
        messages.success(request, 'Ladies measurement saved')
        return redirect('customer_measurements')

    return render(request, 'customer/form.html', {
        'form':  form,
        'title': 'Add Ladies Measurement',
    })


# =============================================================================
# CUSTOMER WEBSITE — SERVICE DETAIL & PLACE ORDER
# =============================================================================

@customer_required
def customer_service_detail(request, service_id):
    service      = get_object_or_404(Service, id=service_id, is_active=True)
    latest_price = service.prices.first()   # ordered by -created_at in Meta
    price        = latest_price.price if latest_price else 0

    return render(request, 'customer/service_detail.html', {
        'service': service,
        'price':   price,
    })


@customer_required
def place_order(request, service_id):
    customer         = get_object_or_404(Customer, id=request.session['customer_id'])
    service          = get_object_or_404(Service, id=service_id, is_active=True)
    latest_price     = service.prices.first()   # ordered by -created_at in Meta
    price            = latest_price.price if latest_price else 0
    men_measurements    = MenMeasurement.objects.filter(customer=customer).order_by('-id')
    ladies_measurements = LadiesMeasurement.objects.filter(customer=customer).order_by('-id')

    if request.method == 'POST':
        delivery_date  = request.POST.get('delivery_date')
        quantity       = int(request.POST.get('quantity', 1) or 1)
        notes          = request.POST.get('notes', '')
        measurement_ref = request.POST.get('measurement_ref')

        # Delivery address fields
        full_name      = request.POST.get('full_name', '')
        contact_phone  = request.POST.get('contact_phone', '')
        pincode        = request.POST.get('pincode', '')
        city           = request.POST.get('city', '')
        house_no       = request.POST.get('house_no', '')
        area           = request.POST.get('area', '')
        landmark       = request.POST.get('landmark', '')
        address_type   = request.POST.get('address_type', 'Home')
        payment_method = request.POST.get('payment_method', 'Cash on Delivery')
        advance_amount = int(request.POST.get('advance_amount', 0) or 0)

        # Validate measurement selection
        if not measurement_ref:
            messages.error(request, 'Please select your saved measurement.')
            return redirect('place_order', service_id=service.id)

        try:
            measurement_type, measurement_id = measurement_ref.split('-')
        except ValueError:
            messages.error(request, 'Invalid measurement selected.')
            return redirect('place_order', service_id=service.id)

        if measurement_type == 'men':
            measurement = get_object_or_404(MenMeasurement, id=measurement_id, customer=customer)
            measurement_note = f"Men Measurement ID: {measurement.id}"
        elif measurement_type == 'ladies':
            measurement = get_object_or_404(LadiesMeasurement, id=measurement_id, customer=customer)
            measurement_note = f"Ladies Measurement ID: {measurement.id}"
        else:
            messages.error(request, 'Invalid measurement selected.')
            return redirect('place_order', service_id=service.id)

        total_amount = price * quantity

        if advance_amount > total_amount:
            messages.error(request, 'Advance amount cannot be greater than total amount.')
            return redirect('place_order', service_id=service.id)

        balance_amount = total_amount - advance_amount

        full_notes = (
            f"Delivery Name: {full_name}\n"
            f"Phone: {contact_phone}\n"
            f"Pincode: {pincode}\n"
            f"City: {city}\n"
            f"Address: {house_no}, {area}\n"
            f"Landmark: {landmark}\n"
            f"Address Type: {address_type}\n"
            f"Payment Method: {payment_method}\n\n"
            f"Measurement: {measurement_note}\n\n"
            f"Customer Notes:\n{notes}"
        )

        order = Order.objects.create(
            customer=customer,
            delivery_date=delivery_date,
            order_status='Pending',
            total_amount=total_amount,
            advance_amount=advance_amount,
            balance_amount=balance_amount,
            notes=full_notes,
        )

        OrderItem.objects.create(
            order=order,
            service=service,
            quantity=quantity,
            price=price,
        )

        messages.success(request, 'Order placed successfully')
        return redirect('customer_my_orders')

    return render(request, 'customer/place_order.html', {
        'customer':            customer,
        'service':             service,
        'price':               price,
        'men_measurements':    men_measurements,
        'ladies_measurements': ladies_measurements,
    })