from django.urls import path
from .views import  register, login, home, payment, account_registration

app_name = 'fraud_detection'

urlpatterns = [
  path('', home, name = 'index'),
  path('payment', payment, name = 'payment'),
  path('account/register', account_registration, name = 'account_registration'),
  path('register', register, name = 'register'),
  path('login', login, name = 'login'),
]