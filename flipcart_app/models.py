from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# ------------------      1.shop models     ------------------
class shopregmodel(models.Model):
    uname = models.CharField(max_length=30)
    email = models.EmailField()
    oname = models.CharField(max_length=30)
    sname = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    pic = models.FileField(upload_to='flipcart_app/static')

class shopaddmodel(models.Model):
    iname = models.CharField(max_length=30)
    iprice = models.IntegerField()
    idisc= models.CharField(max_length=500)
    category = models.CharField(max_length=50)
    iimage = models.FileField(upload_to='flipcart_app/static')
    sid= models.IntegerField()
# ------------------      2.user models     ------------------
class userregmodel(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token = models.CharField( max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    pic = models.FileField(upload_to='flipcart_app/static')
    phone = models.IntegerField()
    def __str__(self) :
        return self.user