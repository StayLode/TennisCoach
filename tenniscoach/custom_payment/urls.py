from django.urls import path, re_path
from .views import *

app_name = "custom_payment"

urlpatterns = [
    path('checkout/<int:course_id>/', checkout, name='checkout')
]