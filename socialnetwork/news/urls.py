from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('', views.news_home, name='news'),
    path('create', views.create, name='create'),

]
