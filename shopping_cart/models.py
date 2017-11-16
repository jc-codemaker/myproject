from django.db import models
from user.models import User
from goods.models import GoodsInfo

# Create your models here.

class CartInfo(models.Model):
    userinfo = models.ForeignKey(User)
    goodsinfo = models.ForeignKey(GoodsInfo)
    count = models.IntegerField()
    isdelete = models.BooleanField(default=False)
