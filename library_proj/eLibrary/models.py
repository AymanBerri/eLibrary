from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100, default="Unknown")
    isbn = models.CharField(max_length=20, default="N/A")
    genre = models.CharField(max_length=50, default="Unknown")
    publish_date = models.DateField()

    def __str__(self):
        return self.title
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    my_books = models.ManyToManyField(Book, related_name="book_holders")    # watchlist

    def __str__(self):
        return f"{self.pk} {self.user}"