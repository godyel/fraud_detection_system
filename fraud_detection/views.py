from fraud_detection.models import Profile, Transaction
from fraud_detection.decorators import account_completed
from helpers.funcs import controlTransactionView, getCleanErrors
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render,HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from .forms import PaymentForm, UserRegistrationForm, LoginForm, AccountForm
# Create your views here.


def home(request):
 
  
  # if request.method == 'POST':
  #   formSet = UserRegistrationForm(request.POST)
  #   if formSet.is_valid():
  #     # print(formSet.cleaned_data)
  #     formSet.save()
    
    
  return render(request, 'fraud_detection/index.html')


def loginUser(request):
  context = {}
  if request.method == 'POST':
    formSet = LoginForm(request.POST)
    print(request.POST)
    if(formSet.is_valid()):
        username = formSet.cleaned_data.get('username')
        password = formSet.cleaned_data.get('password')
        auth = authenticate(username=username, password=password)
        if  auth is not None:
          login(request, auth)
          ## sessions
          user = User.objects.get(username = username)
          request.session['username'] = username
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

@account_completed
def account_registration(request):
  if request.method == 'POST':
    form = AccountForm(request.POST)
    if form.is_valid():
      
      # print('Form Data', form.cleaned_data)
      form.save()
      print("Form saved")
      return HttpResponseRedirect(reverse('fraud_detection:payment'))
    print(form.errors.as_data())
  return render(request, 'fraud_detection/account_registration.html')


def account_verification(request):
  return render(request, 'fraud_detection/account_verification.html')

@login_required(login_url='/app/login')
def payment(request):
  
  
  context = {}
  if request.method == 'POST':
    print(request.POST)
    form = PaymentForm(request.POST)
    if form.is_valid():
      t = Transaction.objects.create(amount=form.cleaned_data.get('amount'), profile = Profile.objects.get(user = request.user))
      t.save()
      print('Transaction passed')
      return controlTransactionView(request.user)
    else:
      context['error'] = 'Transaction failed,card details is incorrect'
      print(form.errors.as_data())
      
    
  return render(request, 'fraud_detection/payment.html', context)
  
@login_required(login_url='/app/login')
def payment_completed(request):
  return render(request, 'fraud_detection/payment_completed.html')