# Generated by Django 3.1 on 2020-12-09 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20201209_0920'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='banner_pwd',
        ),
    ]