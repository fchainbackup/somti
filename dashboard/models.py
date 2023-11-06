from django.db import models
from django.contrib.auth.models import User
from account.models import CustomUser

# Create your models here.

    

class Dashboard(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    xrp = models.FloatField(default=0.00)
    xlm = models.FloatField(default=0.00)
    algo = models.FloatField(default=0.00)
    cardano = models.FloatField(default=0.00)
    account_balance = models.FloatField(default=0.00)
    def __str__(self):
        return str(self.user) +" - " + str(self.account_balance)