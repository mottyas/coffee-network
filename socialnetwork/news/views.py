from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Publication
from .forms import PublicationForm


# Create your views here.

def news_home(request):
    news = Publication.objects.order_by('-date')
    print(f'news: {news}')

    return render(request, 'news/news.html', {'news': news, 'username': auth.get_user(request).username})


@login_required(login_url='/')
def create(request):
    user_name = auth.get_user(request).username
    error = ''
    if request.method == 'POST':
        form = PublicationForm(request.POST, request.FILES)

        if form.is_valid():

            post = form.save(commit=False)
            post.author = User.objects.get(username=user_name)

            form.save()
            return redirect('news')
        else:
            error = 'Форма была неверной'
    else:
        form = PublicationForm()
    data = {
        'form': form,
        'error': error,
        'username': auth.get_user(request).username,
    }
    return render(request, 'news/create.html', data)
