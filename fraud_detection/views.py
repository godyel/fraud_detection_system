from helpers.funcs import getCleanErrors
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import render,HttpResponseRedirect, reverse
from .forms import UserRegistrationForm, LoginForm, AccountForm
# Create your views here.


def home(request):
 
  
  # if request.method == 'POST':
  #   formSet = UserRegistrationForm(request.POST)
  #   if formSet.is_valid():
  #     # print(formSet.cleaned_data)
  #     formSet.save()
    
    
  return render(request, 'fraud_detection/index.html')


def login(request):
  context = {}
  if request.method == 'POST':
    formSet = LoginForm(request.POST)
    print(request.POST)
    if(formSet.is_valid()):
        username = formSet.cleaned_data.get('username')
        password = formSet.cleaned_data.get('password')
        if authenticate(username=username, password=password) is not None:
          ## sessions
          user = User.objects.get(username = username)
          request.session['fullname'] = user.first_name
          request.session['email'] = user.email
          return HttpResponseRedirect(reverse('fraud_detection:account_registration'))
    else:
      context['err'] = getCleanErrors('username', formSet.errors)
      
  return render(request, 'fraud_detection/login.html', context)

def register(request):
  context = {}
  if request.method == 'POST':
     formSet = UserRegistrationForm(request.POST)
     if formSet.is_valid():
       if(formSet.save()):
         
         return HttpResponseRedirect(reverse('fraud_detection:login'))
       
       
     
     else:
       context = {
         'error': {
           'username': 'username already exists'
         }
       }
  print(context)
  return render(request, 'fraud_detection/register.html', context)

def account_registration(request):
  if request.method == 'POST':
    form = AccountForm(request.POST)
    if form.is_valid():
      
      # print('Form Data', form.cleaned_data)
      form.save()
      print("Form saved")
    
    print(form.errors.as_data())
  return render(request, 'fraud_detection/account_registration.html')

def payment(request):
  if request.method == 'POST':
    print(request.POST)
    
  return render(request, 'fraud_detection/payment.html')
  