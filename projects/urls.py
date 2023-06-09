from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('new/', views.new_project, name='new_project'),
    path('cancel/', views.cancel_project, name='cancel_project'),
    path('reject/', views.reject_project, name='reject_project'),
    path('complete/', views.complete_project, name='complete_project'),
    path('quote/', views.quote_project, name='quote_project'),
    path('testimonial/<int:project_id>/', views.new_testimonial, name='new_testimonial'),
]
