from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'eLibrary'
urlpatterns = [
    path('', views.login_view, name='login'),   # First page the user sees
    path('register/', views.register_view, name="register"),
    path('home/', views.home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(next_page='eLibrary:login'), name='logout'),  #logs out the user
]