from email.policy import default

from django.db import models
from django.contrib.auth.models import User


from account.models import CustomUser
from withdrawal.models import Withdrawal_transact
# Create your models here.



DIFF_CHOICES_TRANS_MODE = (
    ('pending','pending'),
    ('approved','approved'),
)
 
CRYPTO_CHOICE= (
    
    ('XRP','XRP'),
    ('XLM','XLM'),
    ('ALGO','ALGO'),
    ('ADA','ADA'),
   
)
class Deposite(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    ammount = models.FloatField()
    transaction_mode = models.CharField(max_length=11,choices=DIFF_CHOICES_TRANS_MODE)
    cryptos = models.CharField(max_length=7,default="XRP")
    
    date_created =  models.DateTimeField(auto_now_add=True)
    date_of_trade =  models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return str(self.user) + "-" + str(self.ammount)

    

    
    



class Transactions(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    deposite_transact = models.ForeignKey(Deposite,blank=True,null=True,on_delete=models.CASCADE)
    withdrawal_transact = models.ForeignKey(Withdrawal_transact,blank=True,null=True,on_delete=models.CASCADE)
    crypto = models.CharField(max_length=200)
    crypto_address = models.CharField(max_length=200)
    ammount_in_crypto= models.FloatField()
    transaction_type = models.CharField(max_length=200,default="deposite")
    date_created =  models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return str(self.deposite_transact) +" - "+ self.crypto + "-" + str(self.ammount_in_crypto)



class Crypto_for_payments(models.Model):
    crypto = models.CharField(max_length=200)
    crypto_address = models.CharField(max_length=200)
    slug = models.CharField(max_length=200,default="none")

    def __str__(self):
        return str(self.crypto) +" - "+ self.crypto_address 


class Fund_user_wallet_account(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    amount = models.FloatField()
    crypto_types = models.CharField(max_length=7,choices=CRYPTO_CHOICE, default="xrp")
    date_created =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) +" funded "+ str(self.amount)


