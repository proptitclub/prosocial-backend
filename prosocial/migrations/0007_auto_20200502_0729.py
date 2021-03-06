# Generated by Django 3.0.2 on 2020-05-02 07:29

from django.db import migrations, models
import prosocial.models


class Migration(migrations.Migration):

    dependencies = [
        ('prosocial', '0006_comment_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='custommember',
            name='cover',
            field=models.FileField(default='default.jpg', upload_to=prosocial.models.custom_media_path),
        ),
        migrations.AddField(
            model_name='custommember',
            name='gender',
            field=models.BooleanField(null=True),
        ),
    ]
