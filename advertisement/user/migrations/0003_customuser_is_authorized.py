# Generated by Django 4.2.1 on 2023-05-16 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_customuser_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_authorized',
            field=models.BooleanField(default=False),
        ),
    ]
