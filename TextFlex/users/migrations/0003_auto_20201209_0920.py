# Generated by Django 3.1 on 2020-12-09 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_banner_pwd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='banner_pwd',
            field=models.CharField(default='none', max_length=1000),
        ),
    ]
