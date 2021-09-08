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
  

class SecurityQuestion(models.Model):
  id = models.AutoField(primary_key=True)
  question = models.CharField(max_length=50)
  answer = models.CharField(max_length=50)
  
  def __str__(self):
    return '{} - {}'.format(self.id, self.question)

GENDER = (('male', 'Male'), ('female', 'Female'),)
class Profile (models.Model):
  fullname = models.CharField(max_length=200)
  email = models.EmailField(max_length=200)
  address = models.CharField(max_length=100, blank=True)
  city = models.CharField(max_length=100, blank=True)
  dob = models.DateField(blank=True, default=timezone.now())
  gender = models.CharField(max_length=50, choices=GENDER, default='Male')
  user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
  question = models.ManyToManyField(to=SecurityQuestion, blank=True, null=True)
  card = models.OneToOneField(Card, on_delete=models.CASCADE, related_name='profile_card', blank=True, null=True)
  completed = models.BooleanField(default=False,null=True)
  
  def __str__(self):
    return str(self.user.username)
  
  @property
  def get_all_questions(self):
    questions = self.question.all()
    quest = []
    for q in questions:
      quest.append(q)
      
    return quest
  
  
class Transaction(models.Model):
  amount = models.CharField(max_length=9999)
  profile = models.ForeignKey(Profile, related_name='profile', on_delete=models.CASCADE, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return '{} - {}'.format(self.profile, self.amount)
  
  
  @property
  def my_amount(self):
    return self.amount
  
  
  
