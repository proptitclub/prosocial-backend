# Generated by Django 3.0.2 on 2020-04-25 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prosocial', '0004_auto_20200419_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
