from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('api/submit', views.ajax_submit, name='ajax_submit')
]
