from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('detail/<int:pk>', detail, name='detail'),
    path('sms', sms, name='sms'),
]
