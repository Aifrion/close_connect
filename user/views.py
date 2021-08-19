from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    return render(request, 'index.html')

def start(request):
    return redirect('/sign_in')

def sign_in(request):
    return render(request, 'sign_in.html')

def create(request):
    return redirect('/register')

def register(request):
    return render(request, 'register.html')

def check_admin(request):
    return render(request, 'admin.html')