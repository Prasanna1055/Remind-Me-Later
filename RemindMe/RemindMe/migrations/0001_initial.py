# Generated by Django 5.2.2 on 2025-06-08 12:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TODOO',
            fields=[
                ('srno', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('send_via', models.CharField(choices=[('sms', 'SMS'), ('email', 'Email')], default='sms', max_length=10)),
                ('status', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
