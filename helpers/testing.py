import uuid
import pytest
   
def test_card_number_generator(interval = 2, length=16):
  uid = str(uuid.uuid4().int)[0:length]
  start = interval - 1
  str_pattern = ''
  for i in range(len(uid)):
    str_pattern += uid[i]
    if i == start:
      start+=interval
      str_pattern += '-'
  return str_pattern[0:-1]
  

def test_card_number_generator_func():
  ID = test_card_number_generator()
  assert len(ID) == 16

print(test_card_number_generator(4))



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


print(CardData())


GENDER = (('male', 'Male'), ('female', 'Female'),)
print(GENDER[0][1])