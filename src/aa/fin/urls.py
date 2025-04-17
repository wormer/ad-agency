from django.urls import path

from . import views


urlpatterns = [
    path('brand/<int:brand_id>/', views.brand_details, name='brand_details'),
    path('spend/<int:brand_id>/', views.register_spend, name='register_spends'),
]