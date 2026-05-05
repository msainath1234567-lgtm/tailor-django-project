from django.contrib import admin
from .models import *

admin.site.register(Customer)
admin.site.register(Service)
admin.site.register(ServicePrice)
admin.site.register(MenMeasurement)
admin.site.register(LadiesMeasurement)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Gallery)
admin.site.register(ContactEnquiry)
admin.site.register(SiteSetting)
