from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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
    isBaned = models.BooleanField(default=False)
    motto = models.TextField(default="这个人还没有设置个人简介")


class Administrator(models.Model):
    username = models.CharField(max_length=NAME_LEN, primary_key=True)
    password = models.CharField(max_length=PASSWD_LEN)


class Post(models.Model):
    time = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=TITLE_LEN, unique=True)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Notice(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=TITLE_LEN)
    content = models.TextField()
    admin = models.ForeignKey(Administrator, on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=NAME_LEN, unique=True)  # 应该是独特的
    num = models.IntegerField()  # 被引用次数


class Order(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    saler = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saler_order')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_order')
    state = models.IntegerField(default=0)


class CommentOnPeople(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    txt = models.TextField()
    # 设置为1到10之间的评分
    score = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(10)
    ])


class Commodity(models.Model):
    name = models.CharField(max_length=TITLE_LEN)
    description = models.TextField()
    price = models.IntegerField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    # 如果order被删除，这个商品的order被设置为null


class Photo(models.Model):
    file = models.ImageField(upload_to='pic/')
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE, null=True)


class Avator(models.Model):
    file = models.ImageField(upload_to='avator/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    admin = models.ForeignKey(Administrator, on_delete=models.CASCADE, null=True)


# tag_post关系
class Tag_Post(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


# 新功能
class FirstComment(models.Model):
    fromUser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()


class SecondComment(models.Model):
    fromUser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    toComment = models.ForeignKey(FirstComment, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
