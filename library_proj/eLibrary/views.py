from datetime import datetime
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Book, Profile



# Create your views here.

@login_required
@user_passes_test(lambda u: u.is_authenticated, login_url='eLibrary:login') # if user directly puts the home link without loggin in, he is directly directed to login
def home(request):
    books = Book.objects.all()

    return render(request, 'eLibrary/home.html', {
        'books': books,
    })



def book_view(request, book_title):
    # Retrieve the specific book based on the title
    book = get_object_or_404(Book, title=book_title)
    
    # Check if the book is already in the user's watchlist
    is_watchlisted = False
    if request.user.is_authenticated:
        user_profile = Profile.objects.get(user=request.user)
        if book in user_profile.my_books.all():
            is_watchlisted = True
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            user_profile = Profile.objects.get(user=request.user)
            
            if is_watchlisted:
                # Remove the book from the user's watchlist
                user_profile.my_books.remove(book)
                is_watchlisted = False
            else:
                # Add the book to the user's watchlist
                user_profile.my_books.add(book)
                is_watchlisted = True

    
    return render(request, 'eLibrary/book.html', {
        'book': book,
        'is_watchlisted': is_watchlisted,
    })



def watchlist_view(request):
    if request.user.is_authenticated:
        books = request.user.profile.my_books.all()
    else:
        books = []

    return render(request, 'eLibrary/home.html', {'books': books})

def add_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        author = request.POST['author']
        isbn = request.POST['isbn']
        genre = request.POST['genre']
        publish_date = datetime.strptime(request.POST['publish_date'], '%Y-%m-%d').date()
        
        # Create a new book object
        book = Book(title=title, description=description, author=author, isbn=isbn, genre=genre, publish_date=publish_date)
        book.save()

        return redirect('eLibrary:book_view', book_title=book.title)
    
    return render(request, 'eLibrary/add_book.html')


def update_book(request, book_title):
    book = get_object_or_404(Book, title=book_title)

    if request.method == 'POST':
        # updating the book
        book.title = request.POST['title']
        book.description = request.POST['description']
        book.author = request.POST['author']
        book.isbn = request.POST['isbn']
        book.genre = request.POST['genre']
        book.publish_date = datetime.strptime(request.POST['publish_date'], '%Y-%m-%d').date()
        book.save()

        return redirect('eLibrary:book_view', book_title=book.title)
    
    return render(request, 'eLibrary/update_book.html', {
        'book': book
    })


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(username=username, password=password)

        # User authentication failed
        if not user:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'eLibrary/login.html', {
                'error_message':'Invalid username or password'
            })

        login(request, user)

        # Redirect to the home page
        return redirect('eLibrary:home')

    else:
        return render(request, 'eLibrary/login.html')




def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return render(request, 'eLibrary/register.html')

        # Create a new user
        user = User.objects.create_user(username=username, password=password, email=email)

        # Create a new profile for the user
        profile = Profile.objects.create(user=user, email=email)

        # # Optionally, you can perform additional tasks such as login the user
        login(request, user)

        # Redirect to the home page
        return redirect('eLibrary:home')

    else:
        return render(request, 'eLibrary/register.html')

