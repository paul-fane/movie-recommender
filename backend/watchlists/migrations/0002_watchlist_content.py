# Generated by Django 5.1.2 on 2024-10-31 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlists', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='content',
            field=models.BooleanField(default=False),
        ),
    ]
