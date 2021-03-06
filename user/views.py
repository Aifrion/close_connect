from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User, Chat


# Create your views here.
def home(request):
    return redirect('/')


def index(request):
    return render(request, 'index.html')


def start(request):
    return redirect('/login')


def sign_in(request):
    try:
        account = User.objects.get(email=request.POST['email'])
    except:
        messages.error(request, "Email or password is incorrect")
        return redirect('/login')
    if bcrypt.checkpw(request.POST['password'].encode(), account.password.encode()):
        request.session['user_id'] = account.id
        if request.session['user_id'] == 1:
            account.user_level = 9
            account.save()
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
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register')
    else:
        pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            user_level=1,
            email=request.POST['email'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            password=pw,
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
    try:
        level = request.session['user_level']
        if level > 5:
            return redirect('/dashboard/admin')
        else:
            return redirect('/dashboard')
    except:
        return redirect('/login')


def admin_dashboard(request):
    try:
        context = {
            'account_user': User.objects.get(id=request.session['user_id']),
            'users': User.objects.all()
        }
        return render(request, 'dash.html', context)
    except:
        return redirect('/login')


def dashboard(request):
    try:
        context = {
            'account_user': User.objects.get(id=request.session['user_id']),
            'users': User.objects.all()
        }
        return render(request, 'dash.html', context)
    except:
        return redirect('/login')


def show(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        account = User.objects.get(id=request.session['user_id'])
        context = {
            'user': user,
            'account': account,
        }
        return render(request, 'profile.html', context)
    except:
        return redirect('/login')


def new(request):
    try:
        id = request.session['user_id']
        return redirect('/users/new')
    except:
        return redirect('/login')


def add(request):
    try:
        id = request.session['user_id']
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/users/new')
        else:
            pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(
                user_level=1,
                email=request.POST['email'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                password=pw
            )
            return redirect('/check_admin')
    except:
        return redirect('/login')


def profile(request):
    try:
        id = request.session['user_id']
        return render(request, 'profile.html')
    except:
        return redirect('/login')


def new_user(request):
    try:
        id = request.session['user_id']
        return render(request, 'new.html')
    except:
        return redirect('/login')


def remove(request, user_id):
    try:
        id = request.session['user_id']
        user_delete = User.objects.get(id=user_id)
        user_delete.delete()
        return redirect('/check_admin')
    except:
        return redirect('/login')


def admin_update_info(request, user_id):
    try:
        id = request.session['user_id']
        errors = User.objects.info_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/users/edit/{user_id}')
        user = User.objects.get(id=user_id)
        user.email = request.POST['email']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.user_level = request.POST['user_level']
        user.save()
        return redirect('/dashboard/admin')
    except:
        return redirect('/login')


def admin_update_password(request, user_id):
    try:
        id = request.session['user_id']
        pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        errors = User.objects.password_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/users/edit/{user_id}')
        user = User.objects.get(id=user_id)
        user.password = pw
        user.save()
        return redirect('/dashboard/admin')
    except:
        return redirect('/login')


def admin_update_profile_pic(request, user_id):
    try:
        id = request.session['user_id']
        if request.method == 'POST' and request.FILES['upload']:
            profile_pic = request.FILES['upload']
            user = User.objects.get(id=user_id)
            user.profile_pic = profile_pic
            user.save()
        return redirect('/dashboard/admin')
    except:
        return redirect('/login')


def admin_edit(request, user_id):
    try:
        id = request.session['user_id']
        context = {
            'user': User.objects.get(id=user_id)
        }
        return render(request, 'admin_edit.html', context)
    except:
        return redirect('/login')


def update_info(request):
    try:
        errors = User.objects.info_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/users/edit')
        user = User.objects.get(id=request.session['user_id'])
        user.email = request.POST['email']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()
        return redirect('/users/edit')
    except:
        return redirect('/login')


def update_password(request):
    try:
        errors = User.objects.password_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/users/edit')
        user = User.objects.get(id=request.session['user_id'])
        pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user.password = pw
        user.save()
        return redirect('/users/edit')
    except:
        return redirect('/login')


def update_description(request):
    try:
        errors = User.objects.description_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/users/edit')
        user = User.objects.get(id=request.session['user_id'])
        user.description = request.POST['description']
        user.save()
        return redirect('/users/edit')
    except:
        return redirect('/login')


def update_profile_pic(request):
    try:
        if request.method == 'POST' and request.FILES['upload']:
            profile_pic = request.FILES['upload']
            user = User.objects.get(id=request.session['user_id'])
            user.profile_pic = profile_pic
            user.save()
        return redirect('/users/edit')
    except:
        return redirect('/login')


def edit(request):
    try:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
        }
        return render(request, 'edit.html', context)
    except:
        return redirect('/login')


def chat_room(request, account_user_id, user_id):
    try:
        id = request.session['user_id']
        if account_user_id < user_id:
            room_id = f'{account_user_id}{user_id}chat'
        else:
            room_id = f'{user_id}{account_user_id}chat'
        account_user = User.objects.get(id=account_user_id)
        user = User.objects.get(id=user_id)
        account_chats = account_user.chatrooms.all()
        if len(account_chats) > 0 and len(account_chats.filter(room_id=room_id)) != 0:
            account_chat = account_chats.filter(room_id=room_id).first()
            account_chat_messages = account_chat.messages.all()
            context = {
                'account_user_id': account_user_id,
                'user_id': user_id,
                'room_id': room_id,
                'messages': account_chat_messages,
                'account_user': account_user,
                'user': user
            }
        else:
            context = {
                'account_user_id': account_user_id,
                'user_id': user_id,
                'room_id': room_id,
                'message': '',
                'account_user': account_user,
                'user': user
            }
        return render(request, 'chat_room.html', context)
    except:
        return redirect('/login')


def main(request):
    try:
        id = request.session['user_id']
        context = {
            'account_user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'main.html', context)
    except:
        return redirect('/login')
