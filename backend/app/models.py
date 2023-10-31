from django.db import models

# Create your models here.
NAME_LEN = 10  # tag
PASSWD_LEN = 20
WECHAT_LEN = 30
PHONE_LEN = 15
TITLE_LEN = 20  # commodity_name


class User(models.Model):
    username = models.CharField(max_length=NAME_LEN, primary_key=True)
    password = models.CharField(max_length=PASSWD_LEN)
    phone = models.CharField(max_length=PHONE_LEN, blank=True, null=True)  # 可为空
    wechat = models.CharField(max_length=WECHAT_LEN)  # 一个wechat只能注册一个账号，防止恶意注册


class Administrator(models.Model):
    username = models.CharField(max_length=NAME_LEN, primary_key=True)
    password = models.CharField(max_length=PASSWD_LEN)


class Post(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=TITLE_LEN)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Order(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    saler = models.ForeignKey(User, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    saler_info = models.TextField()
    buyer_info = models.TextField()


class Notice(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=TITLE_LEN)
    content = models.TextField()
    admin = models.ForeignKey(Administrator, on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=NAME_LEN)
    num = models.IntegerField()  # 被引用次数


class Photo(models.Model):
    path = models.CharField(max_length=100)


class Commodity(models.Model):
    name = models.CharField(max_length=TITLE_LEN)
    description = models.TextField()
    price = models.IntegerField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    # 如果order被删除，这个商品的order被设置为null


# 关系表

# 一对一联系
class UserPhoto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)


# 一对多联系
class CommodityPhoto(models.Model):
    # 一件商品可能有多张图片
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
