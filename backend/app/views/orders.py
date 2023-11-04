from django.shortcuts import render
from rest_framework.views import APIView, Request
from rest_framework.response import Response

from app.models import *


class CreateOder(APIView):
    def post(self, req: Request):
        data = req.data
        buyer = data['user']
        commodity = data['commodity']
        post = Commodity.objects.get(id=commodity).post  # 查询商品所属的帖子
        saler = Post.objects.get(id=post).user  # 查询帖子所属的用户
        value = 1
        id = -1
        try:
            # 在order表中增添记录
            order = Order.objects.create(
                saler=saler,
                buyer=buyer,
            )
            # 在commodity表中将commodity和order关联起来
            c0 = Commodity.objects.get(id=commodity)
            c0.order = order.id
            c0.save()  # 保存
            value = 0
            id = order.id
        except Exception as e:
            print(e)
        return Response({
            'value': value,
            'order': id,
        })


class CancelOrder(APIView):
    def post(self, req: Request):
        data = req.data
        order = data['order']
        try:
            Order.objects.get(id=order).delete() # 删除order元组
            # 其实好像 on_delete=models.SET_NULL 自动就会设置了
            c0 = Commodity.objects.get(order=order) # 修改commodity元组
            c0.order = None
            c0.save()
            return (0)
        except Exception as e:
            print(e)
            return (1)
