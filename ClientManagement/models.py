from django.db import models
from Accounts.models import Account


class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    client_name = models.CharField(max_length=255)
    client_number = models.CharField(max_length=20)
    client_address = models.CharField(max_length=255, blank=True)
    # client_image = models.ImageField(blank=True, null=True)
    client_date_of_joined = models.DateTimeField(auto_now_add=True)
    active_plan = models.CharField(max_length=255)
    plan_start_date = models.DateField()
    plan_end_date = models.DateField()
    total_amount = models.IntegerField()
    amount_paid = models.IntegerField()
    is_active = models.BooleanField(default=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)


class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    attendance_date = models.DateField(auto_now_add=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='attendances', db_column='client')
