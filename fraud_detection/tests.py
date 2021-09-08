from django.test import TestCase
from django.contrib.auth.models import User
from .models import Card, Profile
from django.contrib.auth import authenticate
# Create your tests here.

class UserTestCase(TestCase):
  @classmethod
  def setUp(cls):
    user = {
      'username': 'Teedari',
      'password': '12345',
      'first_name': 'John Doe'
    }
    user2 = User.objects.create(username=user['username'])
    user2.first_name= user['first_name']
    user2.set_password(user['password'])
    user2.save()
    profile = Profile.objects.all()
    # print(profile)
    
  def test_user_exist(self):
    user = User.objects.get(username='Teedari')
    self.assertEqual(user is not None, True)
    self.assertEqual(user.first_name, 'John Doe')
    
    
  def test_user_login(self):
    user = authenticate(username='Teedari', password='12345')
    self.assertEqual(user is not None, True)
    
  
  def test_user_profile_created(self):
    user = User.objects.get(username='Teedari')
    profile = Profile.objects.all()
    # print(profile)
    s_profile = Profile.objects.get(id=1)
    self.assertEqual(profile is not None, True)
    self.assertEqual(s_profile is not None, True)
    
    
  def test_create_card(self):
    card_info = {
      'amount': '5000',
      'card_number': '1234567890123456',
      'card_serial': 'CAB200200'
    }
    card = Card.objects.create(**card_info)
    card.save()
    prof = Profile.objects.get(id=1)
    prof.card = card
    prof.save()
    
    prof = Profile.objects.get(id=1)
    print(prof.card)
    self.assertEqual(prof.card is not None, True)
    self.assertEqual(card is not None, True)
    self.assertEqual(card.amount, card_info['amount'])
    self.assertEqual(card.card_serial, card_info['card_serial'])
    self.assertEqual(card.card_number, card_info['card_number'])

    
