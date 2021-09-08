from fraud_detection.models import GENDER, Card, Profile
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_slug
from django.contrib.auth import authenticate


class UserRegistrationForm(forms.ModelForm):
  
  fullname = forms.CharField(max_length=100)
  confirm_password = forms.CharField(max_length=100)
  class Meta:
    model = User
    fields = ['fullname','username', 'email', 'password']
    
    
  def save(self, commit=True):
    
    user_info = super().save(commit = False)
    user_info.first_name = self.cleaned_data.get('fullname')
    user_info.set_password(self.cleaned_data.get('password'))
    if commit:
        user_info.save()
    return user_info;
    
  
  
class LoginForm(forms.Form):
  username = forms.CharField(max_length=100)
  password = forms.CharField(max_length=100)
  
  def clean(self):
    request = self.cleaned_data

    try:
      user = User.objects.get(username = request.get('username'))
      
    except:
      raise ValidationError(('User credentials does not exist'.format(request.get('username'))), code='existance')
    return request
  
class AccountForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = '__all__'
    exclude = ['user', 'fullname', 'username']
    
    
  def save(self, commit=True):
    prof = super().save(commit=False)
    data = self.cleaned_data
   
    #update profile
    p = Profile.objects.get(email = data.get('email'))
    p.gender = GENDER[0][0] if data.get('gender') == 'male' else GENDER[1][0]
    p.address = data.get('address')
    p.city = data.get('city')
    p.dob = data.get('dob')
    p.completed = True
    p.user.groups.add(1)
    if commit:
      p.save()
    
      
    return data
  
  
 
class PaymentForm(forms.Form):
  card_number = forms.CharField(max_length=19)
  card_serial = forms.CharField(max_length=7)
  amount = forms.CharField(max_length=99)
  created_at = forms.DateField()
  
  
  