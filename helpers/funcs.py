
import uuid
import pytest
from django.contrib.auth.models import Group
from django.http.response import HttpResponse
from fraud_detection.models import Profile, Transaction
from django.shortcuts import reverse, HttpResponseRedirect



def getFormError(key, errors):
  err = ''
  errs = errors.as_data()['username'][0]
  for e in errs:
    err = e
    
  return err;
  
def getCleanErrors(key, errors):
  t = tuple(errors.as_data()['__all__'][0])
  return t[0]


def card_number_generator(interval = 2, length=16):
  uid = str(uuid.uuid4().int)[0:length]
  start = interval - 1
  str_pattern = ''
  for i in range(len(uid)):
    str_pattern += uid[i]
    if i == start:
      start+=interval
      str_pattern += '-'
  return str_pattern[0:-1]


def card_serial_generator(length=3):
  return  str(uuid.uuid4().int)[0:length]

def CardData():
  return {
    'card_number': card_number_generator(4),
    'card_serial': card_serial_generator(),
    'amount': str(uuid.uuid4().int)[0:5],
  }  
  
def check_card_validation(username):
  pass
  p = Profile.objects.get(user = username)
  
def checkTransactionReachLimit(username, l = 7):
  t = Transaction.objects.filter(profile__user__username= username)
  flag = len(t) == l
  username.groups.add(2)
  username.save()
  print('T:.', t)
  return True if  flag else False


def fraud_check(_username):
  p = Profile.objects.get(user__username = _username)
  flag =  p.user.groups.filter(id = 2) is not None
  # print('Groups ', flag)
  
  if(flag is not None):
    t = Transaction.objects.filter(profile__user= _username)
    pass
  
  return True if flag else False


def controlTransactionView(username, data=[]):
  print('control func')
  if checkTransactionReachLimit(username):
    return HttpResponseRedirect(reverse('fraud_detection:account_verify'))
  elif fraud_check(username) and checkTransactionReachLimit(username, 15):
    return HttpResponseRedirect(reverse('fraud_detection:account_verify'))
  else:
    return HttpResponseRedirect(reverse('fraud_detection:payment_completed'))
  
  


### 9807-7116-1957-7091