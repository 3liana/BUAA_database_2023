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
        post_id = int(data['post_id'])
        value = -1
        commodity_id = -1
        try:
            post = Post.objects.get(id=post_id)
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
    def post(self, req: Request):
        commodity_id = req.data['commodity_id']
        return_data = []
        commodity = Commodity.objects.get(id=commodity_id)
        pictures = Photo.objects.filter(commodity=commodity)
        for item in pictures:
            return_data.append({
                'photo_id': item.id,
                'path': item.file.path,
            })
        return Response({'pictures': return_data})


class AddCommodityPicture(APIView):
    def post(self, req: Request):
        commodity_id = req.data.get('commodity_id')
        value = 0
        pic_id = -1
        try:
            commodity = Commodity.objects.get(id=commodity_id)
            pic = Photo.objects.create(
                file=req.FILES.get('photo'),
                commodity=commodity,
            )
            pic_id = pic.id
            pic.save()
        except Exception as e:
            value = 1
            print(e)
        return Response({
                'value': value,
                'photo_id': pic_id,
            })


class CheckIfOrdered(APIView):
    def post(self, req: Request):
        commodity_id = req.data['commodity_id']
        c0 = Commodity.objects.get(id=commodity_id)
        if c0.order is None:
            return Response(0)
        else:
            return Response(1)
