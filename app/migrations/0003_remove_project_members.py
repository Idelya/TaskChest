# Generated by Django 3.1.4 on 2021-01-09 02:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210103_0335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='members',
        ),
    ]
