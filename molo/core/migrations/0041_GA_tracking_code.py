# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-20 12:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_auto_20160722_1041'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='global_ga_tracking_code',
            field=models.CharField(blank=True, help_text='Global GA tracking code to be used to view analytics on more than one site globally', max_length=255, null=True, verbose_name='Global GA Tracking Code'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='local_ga_tracking_code',
            field=models.CharField(blank=True, help_text='Local GA tracking code to be used to view analytics on this site only', max_length=255, null=True, verbose_name='Local GA Tracking Code'),
        ),
    ]
