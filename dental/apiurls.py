# -*- coding:utf-8 -*-
from django.conf.urls import include
from django.urls import path



urlpatterns = [
    path('', include('userapp.apiurls')),
    path('', include('patientapp.apiurls')),
]

