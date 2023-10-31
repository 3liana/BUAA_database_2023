from django.shortcuts import render
from rest_framework.views import APIView, Request
from rest_framework.response import Response

from app.models import *


def check_wechat(wechat):
    try:
        User.objects.get(wechat=wechat)
        return 1
    except User.DoesNotExist:
        return 0
    # 未注册返回0，已注册返回1


def check_username(username):
    try:
        User.objects.get(username=username)
        return 1
    except User.DoesNotExist:
        try:
            Administrator.objects.get(username=username)
            return 2
        except Administrator.DoesNotExist:
            return 0


class Register(APIView):
    def post(self, request):
        data = request.data
        name = str(data.get('name'))
        password = str(data.get('password'))
        phone = str(data.get('phone'))
        wechat = str(data.get('wechat'))
        if check_username(name) != 0:
            return Response(3)  # 此用户名已被注册
        if check_wechat(wechat) == 1:
            return Response(2)  # 此微信号已注册账号
        try:
            u = User.objects.create(
                name=name,
                password=password,
                phone=phone,
                wechat=wechat,
            )
            u.save()
        except Exception as e:
            print(e)
            return Response(1)  # 数据未成功录入数据库
        return Response(0)


class Login(APIView):
    def post(self, request):
        data = request.data
        name = data.get('name')
        password = data.get('password')
        value = 0
        type = -1
        try:
            item = User.objects.get(username=name)
            type = 0  # 普通用户
        except User.DoesNotExist:
            try:
                item = Administrator.objects.get(username=name)
                type = 1  # 管理员
            except Administrator.DoesNotExist:
                value = 1  # 此用户名不存在
        # 用户存在
        if value == 0:
            if password != item.password:
                value = 2  # 密码错误
            else:
                # 成功登录
                request.session['name'] = name
                request.session['type'] = type
        return Response({'value': value, 'type': type})
