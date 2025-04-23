from django.db import models
from django.apps import apps
#from news.models import Publication
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse

from django.contrib.auth.forms import UserCreationForm
from .forms import EditProfileForm, UserRegisterForm, ProfileForm
from .models import Contact

# Create your views here.
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def login(request):
    """Функция для авторизации в системе"""
    args = {}

    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('news')
        else:
            args['login_error'] = "Такого пользователя не существует"
            return render(request, 'users/login.html', args)
    else:
        return render(request, 'users/login.html', args)


def logout(request):
    auth.logout(request)
    return redirect('news')


@login_required(login_url='/')
def profile(request):
    username = auth.get_user(request).username
    user = User.objects.get(username=username)
    news = apps.get_model('news', 'Publication').objects.filter(author=user).order_by('-date')
    return render(request, 'users/profile.html', {'user': user, 'news': news})


@login_required(login_url='/')
def edit_profile(request):
    user_name = auth.get_user(request).username
    user_set = User.objects.get(username=user_name)
    print(user_set.profile.city)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_set.profile)
        if form.is_valid():
            user_setting = request.user
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            status = form.cleaned_data['status']
            avatar = form.cleaned_data['avatar']
            gender = form.cleaned_data['gender']
            city = form.cleaned_data['city']
            birth_date = form.cleaned_data['birth_date']

            if avatar:
                user_setting.profile.avatar = avatar
            else:
                user_setting.profile.avatar = 'images/avatar/default_avatar.jpg'
            user_setting.profile.gender = gender
            user_setting.profile.city = city
            user_setting.profile.status = status

            user_setting.profile.birth_date = birth_date
            if first_name:
                user_setting.first_name = first_name
            if last_name:
                user_setting.last_name = last_name
            user_setting.save()
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=user_set.profile)
    context = {'form': form}
    return render(request, 'users/edit_profile.html', context)


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if form.is_valid():
            ins = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = auth.authenticate(username=username, password=password)
            user.profile.avatar = 'images/avatar/default_avatar.jpg'
            ins.first_name = first_name
            ins.last_name = last_name
            ins.save()
            form.save_m2m()
            messages.success(request, 'Вы успешно зарегистрировались!')
            auth.login(request, user)
            return redirect('news')
    else:
        form = UserRegisterForm()

    context = {'form': form}
    return render(request, 'users/register.html', context)


@login_required(login_url='/')
def contacts(request):
    username = auth.get_user(request).username
    user = User.objects.get(username=username)
    contacts_list = Contact.objects.filter(user=request.user)
    data = {
        'contacts': contacts_list,
        'user': user,
        'username': username,
    }
    return render(request, 'users/contacts.html', data)


@login_required(login_url='/')
def add_contact(request, account_username):
    try:
        user = User.objects.get(username=account_username)
    except:
        raise Http404("Пользователь не найден!")

    is_friend = Contact.objects.filter(user=request.user, users_friend=user)

    if not is_friend:
        add_contact = Contact(user=request.user, users_friend=user)
        add_contact.save()
    return HttpResponseRedirect(reverse('users:contacts'))


@login_required(login_url='/')
def delete_contact(request, account_username):
    try:
        user = User.objects.get(username=account_username)
    except:
        raise Http404("Пользователь не найден!")

    new_friend = Contact.objects.filter(user=request.user, users_friend=user )
    new_friend.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/')
def user(request, account_username):

    try:
        user = User.objects.get(username=account_username)
    except:
        raise Http404("Пользователь не найден!")
    user_name = auth.get_user(request).username
    user_self = User.objects.get(username=user_name)

    if auth.get_user(request).username == account_username:
        return profile(request)

    if Contact.objects.filter(user=request.user, users_friend=user):
        is_friend = False
    else:
        is_friend = True

    if not user.profile.avatar:
        user.profile.avatar = 'images/avatar/default_avatar.jpg'

    news = apps.get_model('news', 'Publication').objects.filter(author=user).order_by('-date')
    context = {'other_user': user, 'is_friend': is_friend, 'user': user_self, 'news': news, 'username': account_username }
    return render(request, 'users/user.html', context)


@login_required(login_url='/')
def find_contact(request):
    all_users = []
    if request.method == 'POST':
        name = request.POST.get('name')
        print(name)

        if name != '':
            all_users = (User.objects.filter(first_name=name) | User.objects.filter(last_name=name))
        else:
            all_users = User.objects.filter()

        context = {'users': all_users}
        print(all_users)
        return render(request, 'users/find_users.html', context)
    else:
        return HttpResponseRedirect(reverse('users:contacts'))
