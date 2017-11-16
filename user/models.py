from django.db import models

# Create your models here.
class User(models.Model):
    uname = models.CharField(primary_key=True,max_length=20,unique=True)
    upwd = models.CharField(max_length=42)
    uemail = models.CharField(max_length =100)
    ureceive = models.CharField(max_length = 100,default = '')
    uaddress = models.CharField(max_length = 100,default = '')
    uzipcode = models.CharField(max_length = 6,default = '')
    uphone = models.CharField(max_length = 11,default = '')

    def __str__(self):
        return self.uname
