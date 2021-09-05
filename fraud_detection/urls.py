from django.urls import path
from .views import  register, login, home, payment

app_name = 'fraud_detection'

urlpatterns = [
  path('', home, name = 'index'),
  path('payment', payment, name = 'payment'),
  path('register', register, name = 'register'),
  path('login', login, name = 'login'),
]