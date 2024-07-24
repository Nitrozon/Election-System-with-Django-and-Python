from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import Voters

class AdmissionNumberBackend(BaseBackend):
    def authenticate(self, request, admission_no=None):
        try:
            voter = Voters.objects.get(admission_no=admission_no)
            user, created = User.objects.get_or_create(username=admission_no)
            return user
        except Voters.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
