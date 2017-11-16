from django.db import models
from user.models import *

# Create your models here.

class OrderInfo(models.Model):
    oid = models.CharField(max_length = 60, primary_key = True)
    userinfo = models.ForeignKey(User)
    odate = models.DateTimeField(auto_now_add = True)
    oispay = models.BooleanField(default = False)
    ototal = models.DecimalField(max_digits = 10,decimal_places = 2)
    oaddress = models.CharField(max_length = 150,default = '')

class OrderDetailInfo(models.Model):
    goodsinfo = models.ForeignKey('goods.GoodsInfo')
    orderinfo = models.ForeignKey(OrderInfo)
    price = models.DecimalField(max_digits = 10,decimal_places =2)
    count = models.IntegerField()