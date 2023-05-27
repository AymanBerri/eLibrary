from django.contrib import admin
from .models import User, Book, Profile

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):

    filter_horizontal= ('my_books',)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Book)