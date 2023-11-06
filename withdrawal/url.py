from django.urls import path
from .views import withdraw,complete_withdrawal




app_name = "withdrawal"

urlpatterns = [
    path('',withdraw,name='withdrawal-page'),
    path('complete-withdrawal/',complete_withdrawal,name='complete-withdrawal'),
]