from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

def no_permission(request):
    return render(request, 'no_permission.html')
