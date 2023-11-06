from django.shortcuts import render
from .models import Dashboard
from deposite.models import Transactions
from account.models import Profile
from django.contrib.auth.decorators import login_required
from requests import Request,Session
import json
import pprint


def get_crypto_price(coin):
    try:
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
    
        result = json.loads(response.text)["data"][coin][0]["quote"]["USD"]["price"]

        
    except Exception as error:
        result = "NAN"
        
   
    return result
# Create your views here.

@login_required
def dashboard(request):
    user = request.user
    user_dashboard = Dashboard.objects.get(user=user)
    profile_name = Profile.objects.get(user=user)
    # getting user transactions
    user_transaction = Transactions.objects.filter(user=user)

    
    try:
        ammount_in_btc = user_dashboard.account_balance / float(get_crypto_price("BTC"))
    except:
        ammount_in_btc = "NAN"

    assets = {
        "xlm":{
            "amount":user_dashboard.xlm,
            "price":get_crypto_price("XLM")
        },
        "xrp":{
            "amount":user_dashboard.xrp,
            "price":get_crypto_price("XRP")
        },
        "algo":{
            "amount":user_dashboard.algo,
            "price":get_crypto_price("ALGO")
        },
        "cardano":{
            "amount":user_dashboard.cardano,
            "price":get_crypto_price("ADA")
        },
    }
    
    referral = "https://qfsledger.digital/ref/"+str(profile_name.profile_name)
    return render(request,"dashboard/index.html",{"user":user,"user_dashboard":user_dashboard,"referral":referral,"btc_balnce":ammount_in_btc,"assets":assets,"user_transaction":user_transaction})