# Generated by Django 4.1.2 on 2023-03-11 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connection_app', '0002_remove_user_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
