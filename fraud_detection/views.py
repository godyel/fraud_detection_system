from django.http.response import JsonResponse
from fraud_detection.models import Profile, SecurityQuestion, Transaction
from fraud_detection.decorators import account_completed, incompleted_transaction
from helpers.funcs import  getCleanErrors,  get_group, remove_user_from_group
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
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

def logoutUser(request):
  request.session.clear()
  logout(request)
  return HttpResponseRedirect(reverse('fraud_detection:login'))  

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
          request.session['count'] = 6
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
    data = request.POST
    print('Form Data',data.get('question1'))
    
    q1 = data.get('question1')
    a1 = data.get('answer1')
    Q1 = SecurityQuestion(question=q1, answer=a1)
    Q1.save()
    q2 = data.get('question2')
    a2 = data.get('answer2')
    Q2 = SecurityQuestion(question=q2, answer=a2)
    Q2.save()
    q3 = data.get('question3')
    a3 = data.get('answer3')
    Q3 = SecurityQuestion(question=q3, answer=a3)
    Q3.save()
    
    
    #####
    
    
    
    form = AccountForm(request.POST)
    if form.is_valid():
      
      print('Form Data', form.cleaned_data)
      form.save()
      print("Form saved")
      
      instance = Profile.objects.get(user = request.user)
      # instance = form.cleaned_data
      instance.question.add(Q1, Q2)
      instance.question.add(Q3)
      instance.save()
      
      print('Questions saved')
      
      return HttpResponseRedirect(reverse('fraud_detection:payment'))
    print(form.errors.as_data())
  return render(request, 'fraud_detection/account_registration.html')




def account_verification(request):
  context = {}
  question_flag = True
  q = Profile.objects.get(user = request.user)
  context['questions'] = q.get_all_questions
  t = None
  try:
    t = Transaction.objects.get(id = request.session['last_trans_id'])

  except:
    print('Last transaction not found')
  
  if request.method == 'POST':
    data = [request.POST.get(q) for q in request.POST if q != 'csrfmiddlewaretoken']
    print(data)
    for key  in  range(len(context['questions'])):
      if str(context['questions'][key].answer).lower() != str(data[key]).lower():
        question_flag = False
        
    if not question_flag:
      print(t)
      t.delete()
      remove_user_from_group(get_group('in_complete_transaction'), request.user)
      print('transaction deleted successfully', 'user does not have any ')
      
    
    
        
    if question_flag:
      t.completed = True
      t.save()
      print('transaction completed successfully')
      return HttpResponseRedirect(reverse('fraud_detection:payment'))
    return HttpResponseRedirect(reverse('fraud_detection:login'))
      
  return render(request, 'fraud_detection/account_verification.html',  context)




@login_required(login_url='/app/login')
@incompleted_transaction
def payment(request):
  
  context = {}
  if request.method == 'POST':
    
    form = PaymentForm(request.POST)
    data = [ request.POST.get(card) for card in request.POST if card != 'csrfmiddlewaretoken' ]
    if form.is_valid():
      profile = Profile.objects.get(user = request.user)
      if profile.card.card_number == data[0] and profile.card.card_serial == data[1]:
        t = Transaction.objects.create(amount=form.cleaned_data.get('amount'), profile = profile)
        t.save()
        request.session['last_trans_id'] = t.id
        profile.user.groups.add(get_group('in_complete_transaction'))
        profile.save()
        request.session['count'] = 5
        return HttpResponseRedirect(reverse('fraud_detection:account_verify'))
      else:
        request.session['count'] = request.session['count'] - 1
        context['error'] = 'Transaction failed,card details is incorrect'
        print(form.errors.as_data())
        
  if request.session['count'] >= 1 and request.session['count'] <= 3:
    context['attempts'] = request.session['count']
  if request.session['count'] <= 0:
    return HttpResponseRedirect(reverse('fraud_detection:login'))

          
  return render(request, 'fraud_detection/payment.html', context)
  
@login_required(login_url='/app/login')
def payment_completed(request):
  return render(request, 'fraud_detection/payment_completed.html')