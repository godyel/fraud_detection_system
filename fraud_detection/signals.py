from helpers.funcs import CardData
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Card, Profile
from django.contrib.auth.models import User



@receiver(post_save, sender = User)
def create_new_profile(sender, instance, created, **kwargs):
  if created:
   
    profile = Profile.objects.create(fullname = instance.first_name, email = instance.email, user=instance)
    p = profile.save()
    print('Profile created successfully')
    
    
    
@receiver(post_save, sender = Profile)
def create_new_card(sender, instance, created, **kwargs):
  if created:
    data = CardData()
    card = Card.objects.create(card_number=data['card_number'], card_serial=data['card_serial'], amount=data['amount'])
    card.save()
    instance.card = card
    instance.save()
    print('card created successfully')
   