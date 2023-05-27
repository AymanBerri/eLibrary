from django.contrib import admin
from .models import User, Book, Profile

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', )
    filter_horizontal= ('my_books',)
    search_fields = ('user__username',)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Book)