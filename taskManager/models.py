from django.db import models


class AdminAccounts(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200, unique=True)  # Reduced length
    phone = models.CharField(max_length=100)  # Reduced length
    password = models.CharField(max_length=200)

    class Meta:
        db_table = 'admin_accounts'

    def __str__(self):
        return self.name


class Accounts(models.Model):
    name = models.CharField(max_length=100)
    adminId = models.ForeignKey(AdminAccounts, on_delete=models.CASCADE, default=1)
    email = models.EmailField(max_length=200, unique=True)  # Reduced length
    phone = models.CharField(max_length=100)  # Reduced length
    password = models.CharField(max_length=200)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'accounts'

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    adminId = models.ForeignKey(AdminAccounts, on_delete=models.CASCADE, default=1)
    userId = models.ForeignKey(Accounts, on_delete=models.CASCADE, default=1)
    date = models.DateTimeField(null=True)  # Changed to DateTimeField
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'tasks'

    def __str__(self):
        return self.name


