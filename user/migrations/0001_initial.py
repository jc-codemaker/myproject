# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('uname', models.CharField(unique=True, serialize=False, primary_key=True, max_length=20)),
                ('upwd', models.CharField(max_length=42)),
                ('uemail', models.CharField(max_length=100)),
                ('ureceive', models.CharField(default='', max_length=100)),
                ('uaddress', models.CharField(default='', max_length=100)),
                ('uzipcode', models.CharField(default='', max_length=6)),
                ('uphone', models.CharField(default='', max_length=11)),
            ],
        ),
    ]
