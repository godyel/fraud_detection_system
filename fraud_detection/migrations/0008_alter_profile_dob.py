# Generated by Django 3.2.7 on 2021-09-14 21:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('fraud_detection', '0007_auto_20210914_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='dob',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 9, 14, 21, 6, 12, 593608, tzinfo=utc)),
        ),
    ]