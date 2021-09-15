from fraud_detection.models import Profile
import pytest



def test_profile():
  p = Profile.objects.get(user__username='teedari')
  assert p is not None == True

