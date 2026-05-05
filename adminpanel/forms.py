from django import forms
from django.contrib.auth.hashers import make_password
from .models import (
    Customer, Service, ServicePrice,
    MenMeasurement, LadiesMeasurement,
    Order, OrderItem, Payment, Gallery,
    ContactEnquiry, SiteSetting
)

BOOTSTRAP_CLASS = 'form-control'


class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.ClearableFileInput)):
                field.widget.attrs.update({'class': BOOTSTRAP_CLASS})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(field.widget, forms.ClearableFileInput):
                # Style the file input; keep accept restricted to images
                field.widget.attrs.update({
                    'class': 'form-control',
                    'accept': 'image/*',
                })


class CustomerForm(BaseModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {'password': forms.PasswordInput(render_value=True)}

    def save(self, commit=True):
        customer = super().save(commit=False)
        raw_password = self.cleaned_data.get('password')
        if raw_password and not raw_password.startswith('pbkdf2_'):
            customer.password = make_password(raw_password)
        if commit:
            customer.save()
        return customer


class CustomerRegisterForm(BaseModelForm):
    class Meta:
        model = Customer
        fields = ['full_name', 'phone', 'email', 'password', 'gender', 'address', 'city', 'pincode']
        widgets = {'password': forms.PasswordInput()}

    def save(self, commit=True):
        customer = super().save(commit=False)
        customer.password = make_password(self.cleaned_data['password'])
        if commit:
            customer.save()
        return customer


class CustomerLoginForm(forms.Form):
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': BOOTSTRAP_CLASS, 'placeholder': 'Phone number'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': BOOTSTRAP_CLASS, 'placeholder': 'Password'})
    )


class ServiceForm(BaseModelForm):
    class Meta:
        model = Service
        fields = '__all__'


class ServicePriceForm(BaseModelForm):
    class Meta:
        model = ServicePrice
        fields = '__all__'
        widgets = {'effective_from': forms.DateInput(attrs={'type': 'date'})}


# ─────────────────────────────────────────────────────────────────────────────
#  Measurement Forms  (photo_front / photo_back / photo_side added)
# ─────────────────────────────────────────────────────────────────────────────

class MenMeasurementForm(BaseModelForm):
    class Meta:
        model = MenMeasurement
        fields = '__all__'
        # Keeps all numeric fields + notes + the three photo fields.
        # No extra widget overrides needed — BaseModelForm handles file inputs.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add helpful placeholder hints for photo fields
        for photo_field in ('photo_front', 'photo_back', 'photo_side'):
            if photo_field in self.fields:
                self.fields[photo_field].required = False
                self.fields[photo_field].help_text = (
                    'Upload a clear photo (JPG / PNG). Optional but recommended.'
                )


class LadiesMeasurementForm(BaseModelForm):
    class Meta:
        model = LadiesMeasurement
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for photo_field in ('photo_front', 'photo_back', 'photo_side'):
            if photo_field in self.fields:
                self.fields[photo_field].required = False
                self.fields[photo_field].help_text = (
                    'Upload a clear photo (JPG / PNG). Optional but recommended.'
                )


# ─────────────────────────────────────────────────────────────────────────────

class OrderForm(BaseModelForm):
    class Meta:
        model = Order
        exclude = ['created_by', 'balance_amount', 'payment_status']
        widgets = {'delivery_date': forms.DateInput(attrs={'type': 'date'})}


class OrderItemForm(BaseModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'


class PaymentForm(BaseModelForm):
    class Meta:
        model = Payment
        fields = '__all__'


class GalleryForm(BaseModelForm):
    class Meta:
        model = Gallery
        fields = '__all__'


class ContactEnquiryForm(BaseModelForm):
    class Meta:
        model = ContactEnquiry
        fields = '__all__'


class SiteSettingForm(BaseModelForm):
    class Meta:
        model = SiteSetting
        fields = '__all__'