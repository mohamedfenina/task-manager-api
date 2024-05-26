# backends.py
from django.contrib.auth.backends import ModelBackend
from .models import Accounts, AdminAccounts


class AccountBackend(ModelBackend, ):
    def authenticate(self, request, email=None, password=None,role=None, **kwargs):
        global Model
        try:
            print(role)
            if role == "Admin":
                Model = AdminAccounts
            else:
                Model = Accounts

            print(Model)
            account = Model.objects.get(email=email)
            print(account)
            if account.password == password:
                return account
        except Model.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Model.objects.get(pk=user_id)
        except Model.DoesNotExist:
            return None
