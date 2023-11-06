from django.urls import path
from .views import register_user,login_user,update_profile,forget_pass,home,logout_view,submit_email,referral



app_name = "account"

urlpatterns = [
    path('',home,name="home" ),
    path('register_user/',register_user,name="register_user" ),
    path('login/',login_user,name="login_user" ),
    path('logout/',logout_view,name="logout_user" ),
    path('account/',update_profile,name="update_profile" ),
    path('forget_pass/',forget_pass,name="forget_pass" ),
    path('sub_email/',submit_email,name="submit_email" ),
    path('ref/<str:ref_code>/', referral, name='ref'),
    
]
