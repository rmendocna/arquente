# Generated by Django 2.2.10 on 2020-02-10 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0007_auto_20200210_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='slug',
            field=models.SlugField(blank=True, max_length=255),
        ),
    ]
