# Generated by Django 5.1.2 on 2024-11-12 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='youtube_id',
            field=models.CharField(blank=True, max_length=220, null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='state',
            field=models.CharField(choices=[('PU', 'Publish'), ('DR', 'Draft'), ('UN', 'Unlisted'), ('PR', 'Private')], default='DR', max_length=2),
        ),
    ]
