from django.shortcuts import render,redirect
from .models import Crypto_for_payments,Deposite,Transactions
from requests import Request,Session
import json
from django.contrib import messages
import pprint
from django.contrib.auth.decorators import login_required
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

def send_deposite_email(user,ammount):
    
    email_subject = 'New Deposite'
    email_body = render_to_string('deposite/deposite_email.html', {
        'user': user.username,
        'ammount':ammount,
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email='support@qfsledger.digital',
                         to=["adamjojn75@gmail.com"]
                         )
    if not settings.TESTING:
        EmailThread(email).start()

# Create your views here.
@login_required
def deposite(request):
    code = request.GET.get("paywith",None)
    if code and Crypto_for_payments.objects.filter(slug=code).exists():
        crypto = Crypto_for_payments.objects.filter(slug=code)[0]
        if request.method == "POST":
            crypto = Crypto_for_payments.objects.filter(slug=code)[0]
            amount_deposited = request.POST.get("amount")
            price_of_asset = get_crypto_price(code)
            quantity_asset = float(amount_deposited)/float(price_of_asset)
            new_deposite = Deposite(
                user=request.user,
                ammount=amount_deposited,
                transaction_mode="pending",
                cryptos=code
            )
            new_deposite.save()
            new_transaction = Transactions(
                user=request.user,
                deposite_transact=new_deposite,
                crypto=code,
                crypto_address=crypto.crypto_address,
                ammount_in_crypto= quantity_asset,
                transaction_type="deposite"                          
                )
            new_transaction.save()
            send_deposite_email(request.user,amount_deposited)
            messages.success(request, "please wait... while your transaction is been proved")
            return redirect('dashboard:dashboard-page')
        return render(request,'deposite/cormfirm-payment.html',{"crypto":crypto})


    payments_methods = Crypto_for_payments.objects.all()

    return render(request,'deposite/index.html',{"payments_methods":payments_methods})
