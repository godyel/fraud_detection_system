
import uuid
from django.contrib.auth import SESSION_KEY
from django.contrib.sessions import models


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


def card_serial_generator(initial='CVC', length=3):
  return  initial +' '+ str(uuid.uuid4().int)[0:length]

def CardData():
  return {
    'card_number': card_number_generator(4),
    'card_serial': card_serial_generator(),
    'amount': str(uuid.uuid4().int)[0:5],
  }  