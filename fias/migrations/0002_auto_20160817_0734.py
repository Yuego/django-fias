# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fias', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='addrobj',
            name='cadnum',
            field=models.CharField(max_length=100, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='addrobj',
            name='divtype',
            field=models.CharField(max_length=1, default=0),
        ),
        migrations.AddField(
            model_name='house',
            name='cadnum',
            field=models.CharField(max_length=100, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='house',
            name='divtype',
            field=models.CharField(max_length=1, default=0),
        ),
        migrations.AddField(
            model_name='house',
            name='regioncode',
            field=models.CharField(max_length=2, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='landmark',
            name='cadnum',
            field=models.CharField(max_length=100, blank=True, null=True),
        ),
    ]
