from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

date = timezone.now()
class Card(models.Model):
  id = models.AutoField(primary_key=True)
  card_number = models.CharField(max_length=16)
  card_serial = models.CharField(max_length=10)
  amount = models.CharField(max_length=999)
  issued_date = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return '{} -  {}, {}'.format(self.id, self.card_serial, self.amount)
  


GENDER = (('male', 'Male'), ('female', 'Female'),)
class Profile (models.Model):
  fullname = models.CharField(max_length=200)
  email = models.EmailField(max_length=200)
  address = models.CharField(max_length=100, blank=True)
  city = models.CharField(max_length=100, blank=True)
  dob = models.DateField(blank=True, default=timezone.now())
  gender = models.CharField(max_length=50, choices=GENDER, default='Male')
  user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
  card = models.OneToOneField(Card, on_delete=models.CASCADE, related_name='profile_card', blank=True, null=True)
  
  def __str__(self):
    return str(self.fullname)
  
  
class Transaction(models.Model):
  amount = models.CharField(max_length=9999)
  card = models.ForeignKey(Card, related_name='transaction_card', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return '{} - {}'.format(self.card, self.amount)
  
  
  
