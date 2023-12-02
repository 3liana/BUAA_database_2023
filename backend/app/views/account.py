from django.shortcuts import render
from rest_framework.views import APIView, Request
from rest_framework.response import Response
from app.views.util import changePicPath
from app.models import *


def check_wechat(wechat):
    value = 0
    try:
        User.objects.get(wechat=wechat)
    except User.DoesNotExist:
        value = 1  # 具有相同wechat的用户不存在 check通过
    return value == 1


def check_username(username):
    value = 0
    try:
        User.objects.get(username=username)
    except User.DoesNotExist:
        value = 1
        try:
            Administrator.objects.get(username=username)
        except Administrator.DoesNotExist:
            value = 2
    # value == 2 代表 库中不存在此username 即check通过
    return value == 2


class Register(APIView):
    # 普通用户
    def post(self, request):
        data = request.data
        name = str(data.get('name'))
        password = str(data.get('password'))
        phone = str(data.get('phone'))
        wechat = str(data.get('wechat'))
        # name = "ddfsfdd"
        # password = "dwe3443"
        # phone = "3243556"
        # wechat = "fdg23gfdg"
        if not check_username(name):
            return Response({"value": 3})  # 此用户名已被注册
        if not check_wechat(wechat):
            return Response({"value": 2})  # 此微信号已注册账号
        try:
            u = User.objects.create(
                username=name,
                password=password,
                phone=phone,
                wechat=wechat,
            )
            u.save()
        except Exception as e:
            print(e)
            return Response({"value": 1})  # 数据未成功录入数据库
        return Response({"value": 0})


class Login(APIView):
    def post(self, request):
        data = request.data
        print("login data:")
        print(data)  # debug
        name = data.get('name')
        password = data.get('password')
        value = 0
        type = -1
        debug = False
        if (debug):
            all_user = User.objects.all()
            for user in all_user:
                print(user.username)
        try:
            item = User.objects.get(username=name)
            print("user")
            print(item)
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
            elif type == 0 and item.isBaned:
                value = 3
            else:
                # 成功登录
                request.session['name'] = name
                request.session['type'] = type
        return Response({
            'value': value,
            'type': type,
        })


class SetAvator(APIView):
    def post(self, req: Request):
        value = -1
        avator_id = -1
        file = req.FILES.get('photo')
        try:
            username = req.data['username']  # 得到用户名
            user = User.objects.get(username=username)  # 查找用户对象
            try:
                item = Avator.objects.get(user=user)
                item.file = file
                item.save()
                avator_id = item.id
            except Avator.DoesNotExist:
                pic = Avator.objects.create(
                    file=file,
                    user=user,
                )
                pic.save()
                avator_id = pic.id
            value = 0
        except Exception as e:
            print(e)
            value = 1
        return Response({
            'value': value,
            'avator_id': avator_id,
        })


class GetAvator(APIView):
    def post(self, req: Request):
        username = req.data['username']
        path = ''
        try:
            user = User.objects.get(username=username)
            pic = Avator.objects.get(user=user)
            path = pic.file.path
            value = 0
        except Exception as e:
            print(e)
            value = 1
        return Response({
            'value': value,
            'path': path,
            'base64': changePicPath(path)
        })


class SetAvatorAdmin(APIView):
    def post(self, req: Request):
        value = -1
        avator_id = -1
        file = req.FILES.get('photo')
        try:
            username = req.data['username']  # 得到用户名
            user = Administrator.objects.get(username=username)  # 查找用户对象
            try:
                item = Avator.objects.get(admin=user)
                item.file = file
                item.save()
                avator_id = item.id
            except Avator.DoesNotExist:
                pic = Avator.objects.create(
                    file=file,
                    admin=user,
                )
                pic.save()
                avator_id = pic.id
            value = 0
        except Exception as e:
            print(e)
            value = 1
        return Response({
            'value': value,
            'avator_id': avator_id,
        })


class GetAvatorAdmin(APIView):
    def post(self, req: Request):
        username = req.data['username']
        path = ''
        try:
            user = Administrator.objects.get(username=username)
            pic = Avator.objects.get(admin=user)
            path = pic.file.path
            value = 0
        except Exception as e:
            print(e)
            value = 1
        return Response({
            'value': value,
            'path': path,
            'base64': changePicPath(path)
        })


class MyPosts(APIView):
    def post(self, req: Request):
        username = req.data['username']
        # 感觉不用try 只有登录的user才能使用这个功能 所以一定能查找到user
        user = User.objects.get(username=username)
        posts = Post.objects.filter(user=user)
        value = 1 if len(posts) == 0 else 0
        return_data = []
        for item in posts:
            return_data.append(item.id)
        return Response({
            'value': value,
            'post_ids': return_data
        })


class MyOrdersAsSaler(APIView):
    def post(self, req: Request):
        username = req.data['username']
        user = User.objects.get(username=username)
        orders = Order.objects.filter(saler=user)
        value = 1 if len(orders) == 0 else 0
        return_data = []
        for item in orders:
            return_data.append(item.id)
        return Response({
            'value': value,
            'order_ids': return_data,
        })


class MyOrdersAsBuyer(APIView):
    def post(self, req: Request):
        username = req.data['username']
        user = User.objects.get(username=username)
        orders = Order.objects.filter(buyer=user)
        value = 1 if len(orders) == 0 else 0
        return_data = []
        for item in orders:
            return_data.append(item.id)
        return Response({
            'value': value,
            'order_ids': return_data,
        })


class GetPassword(APIView):
    def post(self, req: Request):
        username = req.data['username']
        value = -1
        password = ''
        try:
            user = User.objects.get(username=username)
            password = user.password
            value = 0
        except User.DoesNotExist:
            try:
                admin = Administrator.objects.get(username=username)
                password = admin.password
                value = 0
            except Administrator.DoesNotExist:
                value = 1
        return Response({
            'value': value,
            'password': password,
        })


class ChangePassword(APIView):
    def post(self, req: Request):
        username = req.data['username']
        new_password = req.data['new_password']
        value = -1
        try:
            user = User.objects.get(username=username)
            user.password = new_password
            user.save()
            value = 0
        except User.DoesNotExist:
            try:
                admin = Administrator.objects.get(username=username)
                admin.password = new_password
                admin.save()
                value = 0
            except Administrator.DoesNotExist:
                value = 1
        return ({
            'value': value,
        })


class GetUserInfo(APIView):
    def post(self, req: Request):
        username = req.data['username']
        phone = ''
        wechat = ''
        value = -1
        try:
            user = User.objects.get(username=username)
            phone = user.phone
            wechat = user.wechat
            value = 0
        except Exception as e:
            print(e)
            value = 1
        return Response({
            'value': value,
            'phone': phone,
            'wechat': wechat,
        })


class BanAUser(APIView):
    def post(self, req: Request):
        username = req.data['username']
        value = -1
        try:
            user = User.objects.get(username=username)
            user.isBaned = True
            user.save()
            value = 0
        except Exception as e:
            print(e)
            value = 1
        return Response({
            'value': value
        })


class CheckBan(APIView):
    def post(self, req: Request):
        username = req.data['username']
        value = -1
        isBaned = -1
        try:
            user = User.objects.get(username=username)
            if user.isBaned:
                isBaned = 0
            else:
                isBaned = 1
            value = 0
        except Exception as e:
            print(e)
            value = 1
        return Response({
            'value': value,
            'isBaned': isBaned,
        })


class AllUsers(APIView):
    def post(self, req: Request):
        users = User.objects.all()
        return_data = []
        for user in users:
            return_data.append({
                'username': user.username,
                'password': user.password,
                'phone': user.phone,
                'wechat': user.wechat,
                'isBand': user.isBaned,
            })
        return Response({
            'return_data': return_data
        })
