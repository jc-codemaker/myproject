# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetailInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('count', models.IntegerField()),
                ('goodsinfo', models.ForeignKey(to='goods.GoodsInfo')),
            ],
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('oid', models.CharField(primary_key=True, max_length=20, serialize=False)),
                ('odate', models.DateTimeField(auto_now_add=True)),
                ('oispay', models.BooleanField(default=False)),
                ('ototal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('oaddress', models.CharField(max_length=150, default='')),
                ('user', models.ForeignKey(to='user.User')),
            ],
        ),
        migrations.AddField(
            model_name='orderdetailinfo',
            name='orderinfo',
            field=models.ForeignKey(to='order.OrderInfo'),
        ),
    ]
