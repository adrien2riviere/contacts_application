# Generated by Django 4.1.2 on 2023-03-11 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connection_app', '0003_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
    ]
