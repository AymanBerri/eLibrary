from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Book, Profile



# Create your views here.

def home(request):
    books = Book.objects.all()

    return render(request, 'eLibrary/home.html', {
        'books': books,
    })

def book_view(request, book_title):
    # Retrieve the specific book based on the title
    book = get_object_or_404(Book, title=book_title)

    if request.method == 'POST':
        print(f">>>>>>>>>>>>>>>>>>>> {request.POST}")
        # Get the user's profile
        user_profile = Profile.objects.get(user=request.user)

        # Add the book to the user's my_books
        user_profile.my_books.add(book)
        messages.success(request, 'Book added to your watchlist.')

        return redirect('eLibrary:home')

    return render(request, 'eLibrary/book.html', {'book': book})



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

