# Generated by Django 5.1.2 on 2024-10-17 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie_recommender', '0006_rename_language_movie_name_list_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie_name_list',
            old_name='movies',
            new_name='name',
        ),
    ]
