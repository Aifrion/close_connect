from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User
# Create your views here.
def home(request):
    return redirect('/')
def index(request):
    return render(request, 'index.html')

def start(request):
    return redirect('/login')

def sign_in(request):
    try:
        account = User.objects.get(email = request.POST['email'])
    except:
        messages.error(request, "Email or password is incorrect")
        return redirect('/login')
    if bcrypt.checkpw(request.POST['password'].encode(), account.password.encode()):
        request.session['user_id'] = account.id
        request.session['user_level'] = account.user_level
        request.session['first_name'] = account.first_name
        request.session['last_name'] = account.last_name
        request.session['email'] = account.email
        return redirect('/check_admin')
    messages.error(request, "Email or password is incorrect")
    return redirect('/login')

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'user_level' in request.session:
        del request.session['user_level']
    if 'first_name' in request.session:
        del request.session['first_name']
    if 'last_name' in request.session:
        del request.session['last_name']
    if 'email' in request.session:
        del request.session['email']
    return redirect('/login')

def login(request):
    return render(request, 'login.html')

def create(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register')
    else:
        pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            user_level = 1,
            email = request.POST['email'],
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            password = pw
        )
        if user.id == 1:
            user.user_level = 9
            user.save()
        request.session['user_level'] = user.user_level
        request.session['user_id'] = user.id
        return redirect('/check_admin')

def register(request):
    return render(request, 'register.html')

def check_admin(request):
    level = request.session['user_level']
    if level == 9:
        return redirect('/dashboard/admin')
    else:
        return redirect('/dashboard')

def admin_dashboard(request):
    context = {
        'user': User.objects.get(id = request.session['user_id']),
        'users': User.objects.all()
    }
    return render(request, 'admin_dash.html', context)

def dashboard(request):
    context = {
        'user': User.objects.get(id = request.session['user_id']),
        'users': User.objects.all()
    }
    return render(request, 'dash.html', context)

