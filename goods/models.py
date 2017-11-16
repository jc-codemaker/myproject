from django.db import models
from tinymce.models import HTMLField

class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20,unique=True)
    isdelete = models.BooleanField(default=False)

    def __str__(self):
        return self.ttitle

class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20, unique=True)
    gpic = models.ImageField(upload_to='images/goods')
    gprice = models.DecimalField(max_digits=5, decimal_places=2)
    gunit = models.CharField(max_length=20, default='500g')
    gclick = models.IntegerField(default=0)
    gintroduction = models.CharField(max_length=200)
    ttitle = models.CharField(max_length=20, unique=True)
    gstock = models.IntegerField(default=0)
    gcontect = HTMLField()
    gtypeinfo = models.ForeignKey(TypeInfo)
    isdelete = models.BooleanField(default=False)

    def __str__(self):
        return self.gtitle
