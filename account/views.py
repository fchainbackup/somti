from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseNotFound

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required


import email
import threading
from django.urls import reverse
from django.conf import settings
from .models import CustomUser,Profile
from django.http import JsonResponse,HttpResponse
import traceback

from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
# Create your views here.

class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def send_activation_email(user,password,request):
    current_site = get_current_site(request)
    email_subject = 'Registration Info'
    email_body = render_to_string('account/activate_email.html', {
        'user': user.username,
        'firstname':user.first_name,
        'password':password,
        'domain': current_site,
        
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email='support@qfsledger.digital',
                         to=[user.email]
                         )
    if not settings.TESTING:
        EmailThread(email).start()
        
def forget_pass_send_email(user,password,request):
    current_site = get_current_site(request)
    email_subject = 'User Info'
    email_body = render_to_string('account/send_pass.html', {
        'user': user.username,
        'firstname':user.first_name,
        'password':password,
        'domain': current_site,
        
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email='support@qfsledger.digital',
                         to=[user.email]
                         )
    if not settings.TESTING:
        EmailThread(email).start()
def email_sub_access(email):
    
    email_subject = 'Site visited'
    email_body = render_to_string('account/site_access.html', {
        'email': email,
    
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email='support@qfsledger.digital',
                         to=['adamjojn75@gmail.com']
                         )
    if not settings.TESTING:
        EmailThread(email).start()


def register_user(request):
    profile_id = request.session.get('ref_profile_id')

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        # check whether it's valid:
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        country = request.POST.get("country")
        password = request.POST.get("password")
       
        if profile_id is not None:
            recommended_profile = Profile.objects.get(id=profile_id)
            
            try:
                user_reg = CustomUser(
                username = username,
                first_name= first_name,
                last_name = last_name,
                email = email,
                nationality = country,
                password_forget = password
                )
                
                user_reg.set_password(password)
                user_reg.save()
                # update refered user
                registered_user = CustomUser.objects.get(id=user_reg.id)
                registered_user_profile = Profile.objects.get(user=registered_user)
                registered_user_profile.recommended_by = recommended_profile.user
                registered_user_profile.save()
                send_activation_email(user_reg,password,request)
                messages.success(request,"Created! now login to continue")
                return redirect('account:login_user')
            except Exception as e:
                msg = traceback.format_exc()
                messages.error(request,msg)
                return render(request,"account/register.html")
            
        else:
            try:
                user_reg = CustomUser(
                    username = username,
                    first_name= first_name,
                    last_name = last_name,
                    email = email,
                    nationality = country,
                    password_forget = password
                )
                
                
                user_reg.set_password(password)
                user_reg.save()
                send_activation_email(user_reg,password,request)
                messages.success(request,"Created! now login to continue")
                return redirect('account:login_user')
            except Exception as e:
                msg = traceback.format_exc()
                messages.error(request,msg)
                return render(request,"account/register.html")
            

            
    return render(request,"account/register.html")


def login_user(request):

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user= authenticate(request, username=username,password=password)
        if user is not None:
             
            login(request,user,)
            messages.success(request,"login successfully")
            return redirect('dashboard:dashboard-page')
            
        messages.error(request,"incorrect username/password try again")
        return redirect('account:login_user')

        
            
    return render(request,"account/login.html")

@login_required
def update_profile(request):
    user_email = request.user.email
    user_info = CustomUser.objects.get(email=user_email)
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        try:
            user_info.username = username
            user_info.first_name = first_name
            user_info.last_name = last_name
            user_info.save()
            
            messages.success(request,"profile updated uccessfully")
            
            return render(request,'account/index.html',{"user_info":user_info})
            
        except Exception as e:
            msg = traceback.format_exc()
            messages.error(request,"username taken")
            return render(request,'account/index.html',{"user_info":user_info})
    

    return render(request,'account/index.html',{"user_info":user_info})

def forget_pass(request):

    if request.method == "POST":
        email = request.POST.get("email")
        user = CustomUser.objects.filter(email = email)
        if user.exists():
            print(user[0].password_forget)
            forget_pass_send_email(user[0],user[0].password_forget,request)
            messages.success(request,"your account details has been sent to your email")
        else:
            messages.error(request,"email not found")
    return render(request,'account/forget_pass.html')

def home(request):
    email_sub = request.session.get('email_sub')
    
    
    return render(request,'account/home.html' ,{"email_sub":email_sub})

def logout_view(request):
    logout(request)
    return redirect('account:home')

def submit_email(request):
    data=request.POST
    data_ = dict(data.lists())
    data_.pop('csrfmiddlewaretoken')
    request.session['email_sub'] = data_["email"][0]
    email_sub_access(data_["email"][0])
    
    return JsonResponse({"results":True})

    
    
    
    

def referral(request,*args, **kwargs):
    code = str(kwargs.get('ref_code'))
    try:
        profiles = Profile.objects.get(profile_name=code)
        request.session['ref_profile_id'] = profiles.id
    except:
        pass
    return redirect(reverse('account:register_user'))