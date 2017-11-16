# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('count', models.IntegerField()),
                ('isdelete', models.BooleanField(default=False)),
                ('goodsinfo', models.ForeignKey(to='goods.GoodsInfo')),
                ('userinfo', models.ForeignKey(to='user.User')),
            ],
        ),
    ]
