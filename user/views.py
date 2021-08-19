from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    return render(request, 'index.html')

def start(request):
    return redirect('/sign_in')

def sign_in(request):
    return render(request, 'sign_in.html')