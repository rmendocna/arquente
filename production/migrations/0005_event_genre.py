# Generated by Django 2.2.10 on 2020-02-10 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0004_auto_20200209_2321'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='genre',
            field=models.CharField(blank=True, choices=[('concerto', 'Concerto'), ('conferencia', 'Conferência'), ('exposicao', 'Exposição'), ('instalacao', 'Instalação'), ('performance', 'Performance')], max_length=20, null=True, verbose_name='Género'),
        ),
    ]
