import os.path

from django.shortcuts import render
from rest_framework.views import APIView, Request
from rest_framework.response import Response
import uuid
import os

from app.models import *


def cal_picture_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return filename


class CreateCommodity(APIView):
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


class GetCommodityPictures(APIView):
    def get(self, req: Request):
        commodity_id = req.data['commodity_id']
        return_data = []
        pictures = Photo.objects.filter(commodity=commodity_id)
        for item in pictures:
            return_data.append({
                'photo_id': item.id,
                'path': item.file.path,
            })
        return Response({'pictures': return_data})


class AddCommodityPicture(APIView):
    def post(self, req: Request):
        try:
            pic = Photo.objects.create(
                file=req.FILES.get('photo'),
                commodity=req.data['commodity'],
            )
            pic.save()
            return Response({
                'value': 0,
                'photo_id': pic.id,
            })
        except Exception as e:
            print(e)
            return Response({
                'value': 1,
                'photo_id': -1,
            })


class CheckIfOrdered(APIView):
    def post(self, req: Request):
        commodity = req.data['commodity']
        c0 = Commodity.objects.get(id=commodity)
        if c0.order is None:
            return Response(0)
        else:
            return Response(1)
