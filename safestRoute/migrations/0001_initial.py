# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccidentData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('count', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='accidentdata',
            unique_together=set([('latitude', 'longitude')]),
        ),
    ]
