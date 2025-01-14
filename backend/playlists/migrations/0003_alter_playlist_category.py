# Generated by Django 5.1.2 on 2024-10-31 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('playlists', '0002_remove_playlist_category_playlist_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='playlists', to='categories.category'),
        ),
    ]
