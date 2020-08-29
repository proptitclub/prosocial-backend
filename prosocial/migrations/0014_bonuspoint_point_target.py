# Generated by Django 3.0.2 on 2020-08-29 15:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prosocial', '0013_notification_created_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('description', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=256)),
                ('is_done', models.BooleanField()),
                ('status', models.SmallIntegerField(choices=[(0, 'NOT_SCORED'), (1, 'SCORED'), (2, 'CONFIRM')], default=0)),
                ('assigned_user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('point', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='prosocial.Point')),
            ],
        ),
        migrations.CreateModel(
            name='BonusPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('description', models.CharField(max_length=256)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('assigned_user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
