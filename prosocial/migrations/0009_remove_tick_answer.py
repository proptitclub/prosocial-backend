# Generated by Django 3.0.2 on 2020-05-14 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prosocial', '0008_auto_20200502_0745'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tick',
            name='answer',
        ),
    ]