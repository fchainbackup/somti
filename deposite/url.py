from django.urls import path
from .views import deposite




app_name = "deposite"

urlpatterns = [
    path('',deposite,name='deposite-page'),
]