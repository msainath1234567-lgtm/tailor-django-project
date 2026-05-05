from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    GENDER_CHOICES = [('Men', 'Men'), ('Ladies', 'Ladies')]

    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


class Service(models.Model):
    GENDER_CHOICES = [
        ('Men', 'Men'),
        ('Ladies', 'Ladies'),
        ('Common', 'Common'),
    ]

    DEFAULT_SERVICES = [
        ("Shirt Stitching",           "Men",    "Professional shirt stitching service"),
        ("Pant Stitching",            "Men",    "Custom pant stitching with perfect fitting"),
        ("Blouse Stitching",          "Ladies", "Designer blouse stitching service"),
        ("Chudidar Stitching",        "Ladies", "Chudidar stitching with custom measurements"),
        ("Saree Fall & Pico",         "Ladies", "Saree fall and pico finishing service"),
        ("Alteration",                "Common", "Garment alteration and resizing service"),
        ("Kids Wear Stitching",       "Common", "Kids wear stitching service"),
        ("Uniform Stitching",         "Common", "School, office and staff uniform stitching"),
        ("Wedding / Bridal Tailoring","Common", "Premium wedding and bridal tailoring service"),
    ]

    service_name = models.CharField(max_length=100)
    service_description = models.TextField(blank=True, null=True)
    gender_type = models.CharField(max_length=20, choices=GENDER_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['service_name']

    def __str__(self):
        return self.service_name

    @classmethod
    def seed_default_services(cls):
        """Run this once to populate default services:
           >>> from yourapp.models import Service
           >>> Service.seed_default_services()
        """
        for name, gender, description in cls.DEFAULT_SERVICES:
            cls.objects.get_or_create(
                service_name=name,
                defaults={
                    'service_description': description,
                    'gender_type': gender,
                    'is_active': True,
                }
            )


class ServicePrice(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='prices'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    effective_from = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.service.service_name} - ₹{self.price}'


class MenMeasurement(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    # ── Body measurements ──────────────────────────────────────────────────────
    neck          = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    shoulder      = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    chest         = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    waist         = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    hip           = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    sleeve_length = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    shirt_length  = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    armhole       = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    pant_waist    = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    pant_length   = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    thigh         = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    knee          = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    bottom        = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    notes         = models.TextField(blank=True, null=True)

    # ── Photo uploads ──────────────────────────────────────────────────────────
    photo_front = models.ImageField(
        upload_to='measurements/men/', blank=True, null=True,
        verbose_name='Front Photo'
    )
    photo_back = models.ImageField(
        upload_to='measurements/men/', blank=True, null=True,
        verbose_name='Back Photo'
    )
    photo_side = models.ImageField(
        upload_to='measurements/men/', blank=True, null=True,
        verbose_name='Side Photo'
    )
    # ──────────────────────────────────────────────────────────────────────────

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Men Measurement - {self.customer.full_name}"


class LadiesMeasurement(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    # ── Body measurements ──────────────────────────────────────────────────────
    shoulder        = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    bust            = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    waist           = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    hip             = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    blouse_length   = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    sleeve_length   = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    armhole         = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    neck_front      = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    neck_back       = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    chudidar_length = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    kurti_length    = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    bottom_length   = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    thigh           = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    knee            = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    ankle           = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    notes           = models.TextField(blank=True, null=True)

    # ── Photo uploads ──────────────────────────────────────────────────────────
    photo_front = models.ImageField(
        upload_to='measurements/ladies/', blank=True, null=True,
        verbose_name='Front Photo'
    )
    photo_back = models.ImageField(
        upload_to='measurements/ladies/', blank=True, null=True,
        verbose_name='Back Photo'
    )
    photo_side = models.ImageField(
        upload_to='measurements/ladies/', blank=True, null=True,
        verbose_name='Side Photo'
    )
    # ──────────────────────────────────────────────────────────────────────────

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Ladies Measurement - {self.customer.full_name}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending',   'Pending'),
        ('Stitching', 'Stitching'),
        ('Ready',     'Ready'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    PAYMENT_CHOICES = [
        ('Unpaid',         'Unpaid'),
        ('Partially Paid', 'Partially Paid'),
        ('Paid',           'Paid'),
    ]

    order_no       = models.CharField(max_length=50, unique=True, blank=True)
    customer       = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date     = models.DateTimeField(auto_now_add=True)
    delivery_date  = models.DateField(blank=True, null=True)
    total_amount   = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    advance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_status   = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    payment_status = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default='Unpaid')
    created_by     = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes          = models.TextField(blank=True, null=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    # ------------------------------------------------------------------
    # Order number generator  (ORD00001, ORD00002, …)
    # NOTE: For high-concurrency use, consider a database sequence instead.
    # ------------------------------------------------------------------
    def generate_order_no(self):
        last_order = Order.objects.order_by('-id').first()
        if last_order and last_order.order_no:
            try:
                last_number = int(last_order.order_no.replace('ORD', ''))
            except ValueError:
                last_number = last_order.id
        else:
            last_number = 0
        return f"ORD{last_number + 1:05d}"

    def save(self, *args, **kwargs):
        # Auto-generate order number on first save
        if not self.order_no:
            self.order_no = self.generate_order_no()

        # Recalculate balance and payment status on every save
        self.balance_amount = self.total_amount - self.advance_amount

        if self.total_amount > 0 and self.advance_amount >= self.total_amount:
            self.payment_status = 'Paid'
        elif self.advance_amount > 0:
            self.payment_status = 'Partially Paid'
        else:
            self.payment_status = 'Unpaid'

        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_no


class OrderItem(models.Model):
    STITCHING_CHOICES = [
        ('Pending',    'Pending'),
        ('Cutting',    'Cutting'),
        ('Stitching',  'Stitching'),
        ('Finishing',  'Finishing'),
        ('Ready',      'Ready'),
    ]

    order               = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    service             = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity            = models.PositiveIntegerField(default=1)
    price               = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    item_total          = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stitching_status    = models.CharField(max_length=50, choices=STITCHING_CHOICES, default='Pending')
    special_instruction = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.item_total = self.quantity * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order.order_no} - {self.service.service_name}"


class Payment(models.Model):
    METHOD_CHOICES = [
        ('Cash',          'Cash'),
        ('UPI',           'UPI'),
        ('Card',          'Card'),
        ('Bank Transfer', 'Bank Transfer'),
    ]

    order          = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount         = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_date   = models.DateTimeField(auto_now_add=True)
    remarks        = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-payment_date']

    def __str__(self):
        return f"{self.order.order_no} - ₹{self.amount}"


class Gallery(models.Model):
    CATEGORY_CHOICES = [
        ('Men',    'Men'),
        ('Ladies', 'Ladies'),
        ('Common', 'Common'),
    ]

    title      = models.CharField(max_length=100)
    image      = models.ImageField(upload_to='gallery/')
    category   = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class ContactEnquiry(models.Model):
    STATUS_CHOICES = [
        ('New',       'New'),
        ('Contacted', 'Contacted'),
        ('Closed',    'Closed'),
    ]

    name            = models.CharField(max_length=100)
    phone           = models.CharField(max_length=15, blank=True, null=True)
    email           = models.EmailField(blank=True, null=True)
    subject         = models.CharField(max_length=150, blank=True, null=True)
    message         = models.TextField()
    enquiry_status  = models.CharField(max_length=50, choices=STATUS_CHOICES, default='New')
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class SiteSetting(models.Model):
    shop_name        = models.CharField(max_length=100)
    phone            = models.CharField(max_length=15)
    email            = models.EmailField()
    address          = models.TextField()
    logo             = models.ImageField(upload_to='logo/', blank=True, null=True)
    whatsapp_number  = models.CharField(max_length=15, blank=True, null=True)
    instagram_url    = models.URLField(blank=True, null=True)
    facebook_url     = models.URLField(blank=True, null=True)
    updated_at       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shop_name