# Generated by Django 4.2.1 on 2023-06-03 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_alter_board_options_board_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='board',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
