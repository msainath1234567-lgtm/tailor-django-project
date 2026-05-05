from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_home, name='customer_home'),
    path('register/', views.customer_register, name='customer_register'),
    path('login/', views.customer_login, name='customer_login'),
    path('logout/', views.customer_logout, name='customer_logout'),
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('profile/', views.customer_profile, name='customer_profile'),
    path('orders/', views.customer_my_orders, name='customer_my_orders'),
    path('orders/<int:pk>/', views.customer_order_detail, name='customer_order_detail'),
    path('measurements/', views.customer_measurements, name='customer_measurements'),
    path('measurements/men/add/', views.customer_men_measurement_add, name='customer_men_measurement_add'),
    path('measurements/ladies/add/', views.customer_ladies_measurement_add, name='customer_ladies_measurement_add'),
    path('services/', views.customer_services, name='customer_services'),
    path('gallery/', views.customer_gallery, name='customer_gallery'),
    path('contact/', views.customer_contact, name='customer_contact'),
]
