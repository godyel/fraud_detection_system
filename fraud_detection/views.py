from django.shortcuts import render,HttpResponseRedirect, reverse
from .forms import UserRegistrationForm
# Create your views here.


def home(request):
 
  
  # if request.method == 'POST':
  #   formSet = UserRegistrationForm(request.POST)
  #   if formSet.is_valid():
  #     # print(formSet.cleaned_data)
  #     formSet.save()
    
    
  return render(request, 'fraud_detection/index.html')


def login(request):
  return render(request, 'fraud_detection/login.html')

def register(request):
  
  if request.method == 'POST':
     formSet = UserRegistrationForm(request.POST)
     if formSet.is_valid():
       formSet.save()
       
       return HttpResponseRedirect(reverse('fraud_detection:login'))
     
     print(formSet.errors.as_json())
      
  return render(request, 'fraud_detection/register.html')

def payment(request):
  return render(request, 'fraud_detection/payment.html')
  