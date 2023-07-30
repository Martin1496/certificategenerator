from django.urls import path
from . import views

urlpatterns = [
    path('create-certificate/', views.create_certificate, name='create_certificate'),
    path('verify-certificate/', views.verify_certificate, name='verify_certificate'),
    path('customize-certificate/<int:certificate_id>/', views.customize_certificate, name='customize_certificate'),
]
