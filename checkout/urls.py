from django.urls import path
from . import views


urlpatterns = [
    path('create_payment_intent/', views.create_payment_intent, name='create_payment_intent'),
    path('<int:project_id>/', views.checkout, name='checkout'),
    path('complete/', views.checkout_complete, name='checkout_complete'),
]
