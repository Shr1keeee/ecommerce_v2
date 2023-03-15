from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

from django.http.response import JsonResponse

def home(request):
    return render(request, 'store/index.html')

