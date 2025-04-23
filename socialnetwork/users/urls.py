from django.conf import settings
from django.conf.urls.static import static

from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('contacts/', views.contacts, name='contacts'),
    path('find_contact/', views.find_contact, name='find_contact'),
    path('user_<str:account_username>/add_contact', views.add_contact, name='add_contact'),
    path('delete_contact<str:account_username>/', views.delete_contact, name='delete_contact'),
    path('user_<str:account_username>/', views.user, name='user'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
