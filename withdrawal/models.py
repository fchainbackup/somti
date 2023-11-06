from django.db import models
from django.contrib.auth.models import User
import random
from account.models import CustomUser
# Create your models here.
PAYMENT_MODE = (
    ('pending','pending'),
    ('approved','approved'),
)

class Withdrawal_transact(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    ammount = models.FloatField()
    crypto_for_pay = models.CharField(max_length=20)
    crypto_address = models.CharField(max_length=200)
    payment_mode = models.CharField(max_length=13,choices=PAYMENT_MODE)
   
    def __str__(self):
        return str(self.user) +" - "+ str(self.ammount) 