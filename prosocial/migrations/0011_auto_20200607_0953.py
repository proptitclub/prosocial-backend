# Generated by Django 3.0.5 on 2020-06-07 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prosocial', '0010_grouppro_avatar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='grouppro',
            old_name='avatar',
            new_name='cover',
        ),
    ]
