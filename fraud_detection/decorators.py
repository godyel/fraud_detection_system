from .models import Profile
from django.shortcuts import reverse
from django.http import HttpResponseRedirect


def account_completed(func):
  def wrapper(request, *args, **kwargs):
    print(request.user)
    if not request.user.groups.filter(name = 'users'):
      return func(request, *args, **kwargs)
    return HttpResponseRedirect(reverse('fraud_detection:payment'))
  return wrapper