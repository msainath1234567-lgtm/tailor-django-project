from django.urls import path
from . import views

urlpatterns = [
    # =========================
    # ADMIN PANEL URLS
    # =========================
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('customers/', views.customer_list, name='customers'),
    path('customers/add/', views.customer_form, name='customer_add'),
    path('customers/edit/<int:pk>/', views.customer_form, name='customer_edit'),
    path('customers/delete/<int:pk>/', views.customer_delete, name='customer_delete'),

    path('services/', views.service_list, name='services'),
    path('services/add/', views.service_form, name='service_add'),
    path('services/edit/<int:pk>/', views.service_form, name='service_edit'),
    path('services/delete/<int:pk>/', views.service_delete, name='service_delete'),

    path('prices/', views.price_list, name='prices'),
    path('prices/add/', views.price_form, name='price_add'),
    path('prices/edit/<int:pk>/', views.price_form, name='price_edit'),
    path('prices/delete/<int:pk>/', views.price_delete, name='price_delete'),

    path('orders/', views.order_list, name='orders'),
    path('orders/add/', views.order_form, name='order_add'),
    path('orders/edit/<int:pk>/', views.order_form, name='order_edit'),
    path('orders/delete/<int:pk>/', views.order_delete, name='order_delete'),
    path('orders/item/add/', views.order_item_form, name='order_item_add'),

    path('payments/add/', views.payment_form, name='payment_add'),

    path('measurements/', views.measurement_list, name='measurements'),
    path('measurements/men/add/', views.men_measurement_form, name='men_measurement_add'),
    path('measurements/men/edit/<int:pk>/', views.men_measurement_form, name='men_measurement_edit'),
    path('measurements/ladies/add/', views.ladies_measurement_form, name='ladies_measurement_add'),
    path('measurements/ladies/edit/<int:pk>/', views.ladies_measurement_form, name='ladies_measurement_edit'),

    path('gallery/', views.gallery_list, name='gallery'),
    path('gallery/add/', views.gallery_form, name='gallery_add'),
    path('gallery/edit/<int:pk>/', views.gallery_form, name='gallery_edit'),
    path('gallery/delete/<int:pk>/', views.gallery_delete, name='gallery_delete'),

    path('enquiries/', views.enquiry_list, name='enquiries'),
    path('enquiries/edit/<int:pk>/', views.enquiry_form, name='enquiry_edit'),

    path('reports/', views.reports, name='reports'),
    path('settings/', views.settings_form, name='settings'),

    # =========================
    # CUSTOMER WEBSITE URLS
    # =========================
    path('site/', views.customer_home, name='customer_home'),
    path('site/register/', views.customer_register, name='customer_register'),
    path('site/login/', views.customer_login, name='customer_login'),
    path('site/logout/', views.customer_logout, name='customer_logout'),
    path('site/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('site/profile/', views.customer_profile, name='customer_profile'),

    path('site/services/', views.customer_services, name='customer_services'),
    path('site/services/<int:service_id>/', views.customer_service_detail, name='customer_service_detail'),
    path('site/order/<int:service_id>/', views.place_order, name='place_order'),

    path('site/gallery/', views.customer_gallery, name='customer_gallery'),
    path('site/contact/', views.customer_contact, name='customer_contact'),

    path('site/orders/', views.customer_my_orders, name='customer_my_orders'),
    path('site/orders/<int:pk>/', views.customer_order_detail, name='customer_order_detail'),

    path('site/measurements/', views.customer_measurements, name='customer_measurements'),
    path('site/measurements/men/add/', views.customer_men_measurement_add, name='customer_men_measurement_add'),
    path('site/measurements/ladies/add/', views.customer_ladies_measurement_add, name='customer_ladies_measurement_add'),
]