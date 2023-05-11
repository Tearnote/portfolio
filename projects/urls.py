from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('new/', views.new_project, name='new_project'),
    path('cancel/', views.cancel_project, name='cancel_project')
]
