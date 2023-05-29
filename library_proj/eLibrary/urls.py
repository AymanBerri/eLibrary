from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'eLibrary'
urlpatterns = [
    path('', views.login_view, name='login'),   # First page the user sees
    path('book/<str:book_title>', views.book_view, name="book_view"),   #specifc page view
    
    path('add_book/', views.add_book, name="add_book"),
    path('book/<str:book_title>/update', views.update_book, name="update_book"),   #update page view


    path('register/', views.register_view, name="register"),    #register new user
    path('home/', views.home, name='home'),     # the list of books
    path('logout/', auth_views.LogoutView.as_view(next_page='eLibrary:login'), name='logout'),  #logs out the user
]