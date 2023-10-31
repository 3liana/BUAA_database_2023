from django.shortcuts import render
from rest_framework.views import APIView, Request
from rest_framework.response import Response

from app.models import *


class CreateCommodity:
    def post(self, req: Request):
        data = req.data
        name = data['name']
        description = data['dc']
        price = int(data['price'])
        post = int(data['post_id'])
        value = -1
        commodity_id = -1
        try:
            commodity = Commodity.objects.create(
                name=name,
                description=description,
                price=price,
                post=post,
            )
            commodity_id = commodity.id
            commodity.save()
            value = 0
        except Exception as e:
            print(e)
            value = 1
        return Response({'value': value, 'commodity_id': commodity_id})
