from django import forms
from django.contrib.auth.models import User



class UserRegistrationForm(forms.ModelForm):
  
  fullname = forms.CharField(max_length=100)
  confirm_password = forms.CharField(max_length=100)
  class Meta:
    model = User
    fields = ['fullname','username', 'email', 'password']
    
    
  def create(self):
    user_info = self.cleaned_data
    first_name = self.cleaned_data.get('fullname')
    user_info['first_name'] = first_name
    user_info.pop('fullname')
    user_info.pop('confirm_password')
    user = User.objects.create(user_info)
    user.set_password(user_info.password)
    user.save()
    return user;