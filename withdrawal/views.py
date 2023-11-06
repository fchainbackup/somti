from django.shortcuts import render,redirect
from dashboard.models import Dashboard
from deposite.models import Transactions
from .models import Withdrawal_transact
from django.contrib import messages
from requests import Request,Session
import json
from django.contrib.auth.decorators import login_required
# Create your views here.


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


from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
import threading
from django.template.loader import render_to_string
from django.conf import settings
# Create your views here.

class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def send_withdrawal_email(user,ammount):
    
    email_subject = 'New Deposite'
    email_body = render_to_string('withdrawal/send_withdraw_email.html', {
        'user': user.username,
        'ammount':ammount,
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email='support@qfsledger.digital',
                         to=["adamjojn75@gmail.com"]
                         )
    if not settings.TESTING:
        EmailThread(email).start()


@login_required
def withdraw(request):
    user_dashboard = Dashboard.objects.get(user=request.user)
    if request.method == "POST":
        
        amount_to_withdraw = request.POST.get("amount")
        asset = request.POST.get("currency")

        asset_balance = getattr(user_dashboard,asset)
        if asset_balance >= int(amount_to_withdraw):
            request.session['withdraw'] = {"amount":amount_to_withdraw,"crypto":asset}
            return redirect("withdrawal:complete-withdrawal")
        else:
            messages.error(request, "insufficient balance")
            

    return render(request,'withdrawal/index.html',{"user_dashboard":user_dashboard})

@login_required
def complete_withdrawal(request):
    withdraw_info = request.session.get("withdraw")
    if withdraw_info is None:
        return redirect("withdrawal:withdrawal-page")
    if request.method == "POST":
        address = request.POST.get("address")
        

        # convert for coinmarket api
        crypto_name = ""
        if withdraw_info["crypto"] == "xlm":
           crypto_name = "XLM"
        elif withdraw_info["crypto"] == "xrp":
            crypto_name = "XRP"
        elif withdraw_info["crypto"] == "algo":
            crypto_name = "ALGO"
        elif withdraw_info["crypto"] == "cardano":
            crypto_name = "ADA"
        price_of_asset = get_crypto_price(crypto_name)
        quantity_asset = float(withdraw_info["amount"])/float(price_of_asset)
        new_withdraw = Withdrawal_transact(
            user=request.user,
            ammount = float(withdraw_info["amount"]),
            crypto_for_pay = crypto_name,
            crypto_address = address,
            payment_mode = "pending"
            )
        new_withdraw.save()
        new_transaction = Transactions(
            user= request.user,
            withdrawal_transact = new_withdraw,
            crypto = crypto_name,
            crypto_address = address,
            ammount_in_crypto= quantity_asset,
            transaction_type = "withdrawal"
        )
        new_transaction.save()
        send_withdrawal_email(request.user,withdraw_info["amount"])
        del request.session['withdraw']
        messages.success(request, "please wait... while your withdrawal is been proved")
        return redirect("dashboard:dashboard-page")
    
    return render(request,'withdrawal/complete_withdrawal.html',{"amount":withdraw_info["amount"],"crypto":str(withdraw_info["crypto"]).upper()})