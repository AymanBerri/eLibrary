# Generated by Django 4.1.7 on 2023-06-02 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eLibrary', '0002_alter_profile_my_books'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
