# Generated by Django 4.2.1 on 2023-06-03 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_customuser__code'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ['email'], 'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
    ]
