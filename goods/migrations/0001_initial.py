# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsInfo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('gtitle', models.CharField(unique=True, max_length=20)),
                ('gpic', models.ImageField(upload_to='images/goods')),
                ('gprice', models.DecimalField(max_digits=5, decimal_places=2)),
                ('gunit', models.CharField(max_length=20, default='500g')),
                ('gclick', models.IntegerField(default=0)),
                ('gintroduction', models.CharField(max_length=200)),
                ('ttitle', models.CharField(unique=True, max_length=20)),
                ('gstock', models.IntegerField(default=0)),
                ('gcontect', tinymce.models.HTMLField()),
                ('isdelete', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TypeInfo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('ttitle', models.CharField(unique=True, max_length=20)),
                ('isdelete', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='goodsinfo',
            name='gtypeinfo',
            field=models.ForeignKey(to='goods.TypeInfo'),
        ),
    ]
