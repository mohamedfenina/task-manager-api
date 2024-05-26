# serializers.py
from django.core.validators import validate_email
from rest_framework import serializers
from .models import Accounts, Task, AdminAccounts
from django import forms


class AccountsAdminSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6)

    class Meta:
        model = AdminAccounts
        fields = '__all__'


# forms.py or serializers.py
class AccountSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6)

    class Meta:
        model = Accounts
        fields = ['id', 'name', 'adminId', 'email', 'phone', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If instance is provided, this is an update; make password and adminId optional
        if self.instance:
            self.fields['password'].required = False
            self.fields['adminId'].required = False
        else:
            # Otherwise, it's a creation; make password and adminId required
            self.fields['password'].required = True
            self.fields['adminId'].required = True


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'adminId', 'userId', 'date','status']


class TaskGSerializer(serializers.ModelSerializer):
    userId = AccountSerializer(read_only=True)
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'adminId', 'userId', 'date', 'status']
