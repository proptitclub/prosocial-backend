# Generated by Django 3.0.2 on 2020-09-03 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prosocial', '0017_target_created_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='target',
            name='created_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]