from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from django.core.exceptions import ValidationError

def generate_deposit_id():
    return f"BD-{uuid.uuid4().hex[:6].upper()}"


class UserDatabase(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=generate_deposit_id, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stake_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    btc = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    eth = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    xlm = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ltc = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bch = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ada = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

@receiver(post_save, sender=User)
def create_user_database(sender, instance, created, **kwargs):
    if created:
        UserDatabase.objects.create(user=instance)


class Withdraw(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=generate_deposit_id, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    crypto_asset  = models.CharField(max_length=255, default='btc')
    address = models.CharField(max_length=50)
    status = models.CharField(max_length=10, default='pending', choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ])

class Stake(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    crypto_asset = models.CharField(max_length=255, default='btc')
    btc = models.BooleanField(default=False)
    eth = models.BooleanField(default=False)
    ltc = models.BooleanField(default=False)
    xlm = models.BooleanField(default=False)
    bch =  models.BooleanField(default=False)
    ada = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    maturity_date = models.DateTimeField(null=True, blank=True)
    duration = models.CharField(max_length=10)
    status = models.CharField(max_length=10, default='approved', choices=[
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed')
    ])

class Fund(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    crypto_asset  = models.CharField(max_length=255, default='btc')
    now_id = models.CharField(max_length=50)
    status = models.CharField(max_length=10, default='waiting', choices=[
        ('waiting', 'Waiting'),
        ('confirming', 'Confirming'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired')
    ])