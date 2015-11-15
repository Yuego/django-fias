# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fias', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql='ALTER TABLE fias_house ALTER COLUMN eststatus TYPE SMALLINT USING eststatus::INTEGER',
            reverse_sql=migrations.RunSQL.noop,
            state_operations=[
                migrations.AlterField(
                    model_name='house',
                    name='eststatus',
                    field=models.PositiveSmallIntegerField(default=0),
                ),
            ]
        )
    ]
