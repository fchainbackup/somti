from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Dashboard
from deposite.models import Deposite,Fund_user_wallet_account
from django.contrib.auth.models import User
from withdrawal.models import Withdrawal_transact
from account.models import CustomUser, Profile

from requests import Request,Session
import json


def get_crypto_price(coin):
    url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
    parameter = {
        "symbol":coin,
        "convert":"USD"
    }
    headers={
        "Accepts":"application/json",
        "X-CMC_PRO_API_KEY":"7a8c40c3-377e-4120-8f9e-a6305b1ea962"
    }
    session = Session()
    session.headers.update(headers)
    response = session.get(url,params=parameter)
    #Make a request to the website
   
    return json.loads(response.text)["data"][coin][0]["quote"]["USD"]["price"]

@receiver(post_save, sender=CustomUser)
def create_dashboard(sender, instance, created, **kwargs):
    if created:
        Dashboard.objects.create(user=instance)
        Profile.objects.create(user=instance,profile_name=instance.username)
        

@receiver(post_save, sender=Deposite)
def update_dashboard(sender, instance, created, **kwargs):
    user_deposite = Deposite.objects.filter(user=instance.user)
    total_deposite = 0.0
    deposite_xlm = 0.0
    deposite_xrp = 0.0
    deposite_algo = 0.0
    deposite_ada = 0.0

    for invest in user_deposite:
        if invest.transaction_mode == "approved":
            total_deposite += invest.ammount
            if invest.cryptos == "XLM":
                deposite_xlm += invest.ammount
            elif invest.cryptos == "XRP":
                deposite_xrp += invest.ammount
            elif invest.cryptos == "ALGO":
                deposite_algo += invest.ammount
            elif invest.cryptos == "ADA":
                deposite_ada += invest.ammount
            
    #for withdarwal
    each_withdraw = 0
    withdraw_xlm = 0.0
    withdraw_xrp = 0.0
    withdraw_algo = 0.0
    withdraw_ada = 0.0
    
    user_withdrawals = Withdrawal_transact.objects.filter(user=instance.user)
    for amount in user_withdrawals:
        if amount.payment_mode == "approved":
            each_withdraw += amount.ammount
            if amount.crypto_for_pay == "XLM":
                withdraw_xlm += amount.ammount
            elif amount.crypto_for_pay == "XRP":
                withdraw_xrp += amount.ammount
            elif amount.crypto_for_pay == "ALGO":
                withdraw_algo += amount.ammount
            elif amount.crypto_for_pay == "ADA":
                withdraw_ada += amount.ammount
            
    # for Fund_user_wallet_account
    funded_amount = 0.00
    funded_xlm = 0.0
    funded_xrp = 0.0
    funded_algo = 0.0
    funded_ada = 0.0
    user_fund = Fund_user_wallet_account.objects.filter(user=instance.user)
    for amount_fund in user_fund:
        funded_amount += amount_fund.amount
        if amount_fund.crypto_types == "XLM":
            funded_xlm += amount_fund.amount
        elif amount_fund.crypto_types == "XRP":
            funded_xrp += amount_fund.amount
        elif amount_fund.crypto_types == "ALGO":
            funded_algo += amount_fund.amount
        elif amount_fund.crypto_types == "ADA":
            funded_ada += amount_fund.amount
        



    total_ammount = total_deposite + funded_amount - each_withdraw
    
    price_of_xlm =  get_crypto_price("XLM")
    price_of_xrp =  get_crypto_price("XRP")
    price_of_algo =  get_crypto_price("ALGO")
    price_of_ada =  get_crypto_price("ADA")
    
    
    total_xlm = deposite_xlm + funded_xlm - withdraw_xlm
    total_xrp = deposite_xrp + funded_xrp - withdraw_xrp
    total_algo = deposite_algo + funded_algo - withdraw_algo
    total_ada = deposite_ada + funded_ada - withdraw_algo
    
    
    user_dashboard = Dashboard.objects.get(user=instance.user)
    user_dashboard.account_balance = total_ammount
    user_dashboard.xlm =  int(total_xlm)/float(price_of_xlm)
    user_dashboard.xrp =  int(total_xrp)/float(price_of_xrp)
    user_dashboard.algo =  int(total_algo)/float(price_of_algo)
    user_dashboard.cardano =  int(total_ada)/float(price_of_ada)
    user_dashboard.save()


@receiver(post_save, sender=Fund_user_wallet_account)
def update_dashboard_through_fund_acount(sender, instance, created, **kwargs):
    user_deposite = Deposite.objects.filter(user=instance.user)
    total_deposite = 0.0
    deposite_xlm = 0.0
    deposite_xrp = 0.0
    deposite_algo = 0.0
    deposite_ada = 0.0

    for invest in user_deposite:
        if invest.transaction_mode == "approved":
            total_deposite += invest.ammount
            if invest.cryptos == "XLM":
                deposite_xlm += invest.ammount
            elif invest.cryptos == "XRP":
                deposite_xrp += invest.ammount
            elif invest.cryptos == "ALGO":
                deposite_algo += invest.ammount
            elif invest.cryptos == "ADA":
                deposite_ada += invest.ammount
            
    #for withdarwal
    each_withdraw = 0
    withdraw_xlm = 0.0
    withdraw_xrp = 0.0
    withdraw_algo = 0.0
    withdraw_ada = 0.0
    
    user_withdrawals = Withdrawal_transact.objects.filter(user=instance.user)
    for amount in user_withdrawals:
        if amount.payment_mode == "approved":
            each_withdraw += amount.ammount
            if amount.crypto_for_pay == "XLM":
                withdraw_xlm += amount.ammount
            elif amount.crypto_for_pay == "XRP":
                withdraw_xrp += amount.ammount
            elif amount.crypto_for_pay == "ALGO":
                withdraw_algo += amount.ammount
            elif amount.crypto_for_pay == "ADA":
                withdraw_ada += amount.ammount
            
    # for Fund_user_wallet_account
    funded_amount = 0.00
    funded_xlm = 0.0
    funded_xrp = 0.0
    funded_algo = 0.0
    funded_ada = 0.0
    user_fund = Fund_user_wallet_account.objects.filter(user=instance.user)
    for amount_fund in user_fund:
        funded_amount += amount_fund.amount
        if amount_fund.crypto_types == "XLM":
            funded_xlm += amount_fund.amount
        elif amount_fund.crypto_types == "XRP":
            funded_xrp += amount_fund.amount
        elif amount_fund.crypto_types == "ALGO":
            funded_algo += amount_fund.amount
        elif amount_fund.crypto_types == "ADA":
            funded_ada += amount_fund.amount
        



    total_ammount = total_deposite + funded_amount - each_withdraw
    
    price_of_xlm =  get_crypto_price("XLM")
    price_of_xrp =  get_crypto_price("XRP")
    price_of_algo =  get_crypto_price("ALGO")
    price_of_ada =  get_crypto_price("ADA")
    
    
    total_xlm = deposite_xlm + funded_xlm - withdraw_xlm
    total_xrp = deposite_xrp + funded_xrp - withdraw_xrp
    total_algo = deposite_algo + funded_algo - withdraw_algo
    total_ada = deposite_ada + funded_ada - withdraw_algo
    
    
    user_dashboard = Dashboard.objects.get(user=instance.user)
    user_dashboard.account_balance = total_ammount
    user_dashboard.xlm =  int(total_xlm)/float(price_of_xlm)
    user_dashboard.xrp =  int(total_xrp)/float(price_of_xrp)
    user_dashboard.algo =  int(total_algo)/float(price_of_algo)
    user_dashboard.cardano =  int(total_ada)/float(price_of_ada)
    user_dashboard.save()

@receiver(post_save, sender=Withdrawal_transact)
def update_dashboard_through_withdraw(sender, instance, created, **kwargs):
    user_deposite = Deposite.objects.filter(user=instance.user)
    total_deposite = 0.0
    deposite_xlm = 0.0
    deposite_xrp = 0.0
    deposite_algo = 0.0
    deposite_ada = 0.0

    for invest in user_deposite:
        if invest.transaction_mode == "approved":
            total_deposite += invest.ammount
            if invest.cryptos == "XLM":
                deposite_xlm += invest.ammount
            elif invest.cryptos == "XRP":
                deposite_xrp += invest.ammount
            elif invest.cryptos == "ALGO":
                deposite_algo += invest.ammount
            elif invest.cryptos == "ADA":
                deposite_ada += invest.ammount
            
    #for withdarwal
    each_withdraw = 0
    withdraw_xlm = 0.0
    withdraw_xrp = 0.0
    withdraw_algo = 0.0
    withdraw_ada = 0.0
    
    user_withdrawals = Withdrawal_transact.objects.filter(user=instance.user)
    for amount in user_withdrawals:
        if amount.payment_mode == "approved":
            each_withdraw += amount.ammount
            if amount.crypto_for_pay == "XLM":
                withdraw_xlm += amount.ammount
            elif amount.crypto_for_pay == "XRP":
                withdraw_xrp += amount.ammount
            elif amount.crypto_for_pay == "ALGO":
                withdraw_algo += amount.ammount
            elif amount.crypto_for_pay == "ADA":
                withdraw_ada += amount.ammount
            
    # for Fund_user_wallet_account
    funded_amount = 0.00
    funded_xlm = 0.0
    funded_xrp = 0.0
    funded_algo = 0.0
    funded_ada = 0.0
    user_fund = Fund_user_wallet_account.objects.filter(user=instance.user)
    for amount_fund in user_fund:
        funded_amount += amount_fund.amount
        if amount_fund.crypto_types == "XLM":
            funded_xlm += amount_fund.amount
        elif amount_fund.crypto_types == "XRP":
            funded_xrp += amount_fund.amount
        elif amount_fund.crypto_types == "ALGO":
            funded_algo += amount_fund.amount
        elif amount_fund.crypto_types == "ADA":
            funded_ada += amount_fund.amount
        



    total_ammount = total_deposite + funded_amount - each_withdraw
    
    price_of_xlm =  get_crypto_price("XLM")
    price_of_xrp =  get_crypto_price("XRP")
    price_of_algo =  get_crypto_price("ALGO")
    price_of_ada =  get_crypto_price("ADA")
    
    
    total_xlm = deposite_xlm + funded_xlm - withdraw_xlm
    total_xrp = deposite_xrp + funded_xrp - withdraw_xrp
    total_algo = deposite_algo + funded_algo - withdraw_algo
    total_ada = deposite_ada + funded_ada - withdraw_algo
    
    
    user_dashboard = Dashboard.objects.get(user=instance.user)
    user_dashboard.account_balance = total_ammount
    user_dashboard.xlm =  int(total_xlm)/float(price_of_xlm)
    user_dashboard.xrp =  int(total_xrp)/float(price_of_xrp)
    user_dashboard.algo =  int(total_algo)/float(price_of_algo)
    user_dashboard.cardano =  int(total_ada)/float(price_of_ada)
    user_dashboard.save()