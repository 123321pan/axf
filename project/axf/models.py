from django.db import models

# Create your models here.
class Wheel(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=10)
    trackid = models.CharField(max_length=10)
class Nav(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=10)
    trackid = models.CharField(max_length=10)

class FoodTypes(models.Model):
    typeid = models.CharField(max_length=10)
    typename = models.CharField(max_length=20)
    typesort = models.IntegerField()
    childtypenames = models.CharField(max_length=150)

class Goods(models.Model):
    productid = models.CharField(max_length=10)
    productimg = models.CharField(max_length=150)
    productname = models.CharField(max_length=150)
    productlongname = models.CharField(max_length=100)
    isxf = models.NullBooleanField(default=False)
    pmdesc = models.CharField(max_length=10)
    specifics = models.CharField(max_length=20)
    price = models.CharField(max_length=10)
    marketprice = models.CharField(max_length=10)
    categoryid = models.CharField(max_length=10)
    childcid = models.CharField(max_length=10)
    childcidname = models.CharField(max_length=10)
    dealerid = models.CharField(max_length=10)
    storenums = models.IntegerField()
    productnum = models.IntegerField()

class User(models.Model):
    userAccount = models.CharField(max_length=20,unique=True)
    userPasswd = models.CharField(max_length=20)
    userName = models.CharField(max_length=20)
    userPhone = models.CharField(max_length=20)
    userAddress = models.CharField(max_length=100)
    userImg = models.CharField(max_length=150)
    userRank = models.IntegerField()
    userToken = models.CharField(max_length=50)
    @classmethod
    def creatuser(cls,account,passwd,name,phone,address,img,rank,token):
        u = cls(userAccount=account,userPasswd=passwd,userName=name,userPhone=phone,userAddress=address
                ,userImg=img,userRank=rank,userToken=token)
        return u

class Cart(models.Model):
    userAccount = models.CharField(max_length=20)
    productid = models.CharField(max_length=20)
    productnum = models.CharField(max_length=20)
    productprice = models.CharField(max_length=20)
    isChose = models.IntegerField(default=False)
    productimg = models.CharField(max_length=20)
    productname = models.CharField(max_length=20)
    orderid = models.CharField(max_length=20,default=0)
    isDelete = models.IntegerField(default=False)
    @classmethod
    def creatcart(cls,userAccount,productid,productnum,productprice,isChose,productimg,productname,isDelete):
        c = cls(userAccount=userAccount,productid=productid,productnum=productnum,productprice=productprice,isChose=isChose
                ,productimg=productimg,productname=productname,isDelete=isDelete)
        return c