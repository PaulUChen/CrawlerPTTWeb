# Generated by Django 2.1.3 on 2019-01-30 10:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PTTLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(default='', max_length=50)),
                ('date', models.DateTimeField(default=datetime.datetime(2019, 1, 30, 10, 44, 36, 769221, tzinfo=utc))),
            ],
        ),
    ]
