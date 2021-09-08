from django.urls import path
from .views import  register, loginUser, home, payment, payment_completed, account_registration, account_verification

app_name = 'fraud_detection'

urlpatterns = [
  path('', home, name = 'index'),
  path('payment', payment, name = 'payment'),
  path('payment/completed', payment_completed, name = 'payment_completed'),
  path('account/register', account_registration, name = 'account_registration'),
  path('account/verification', account_verification, name = 'account_verify'),

  path('register', register, name = 'register'),
  path('login', loginUser, name = 'login'),
]