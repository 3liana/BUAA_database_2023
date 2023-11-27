from django.shortcuts import render
from rest_framework.views import APIView, Request
from rest_framework.response import Response

from app.models import *


class CreateTag(APIView):
    def post(self, req: Request):
        data = req.data
        name = data["name"]
        num = 0
        tag_id = -1
        value = -1
        try:
            tag = Tag.objects.create(
                name=name,
                num=num,
            )
            tag_id = tag.id
            value = 0
        except Exception as e:
            print(e)
            value = 1
        return Response({
            'value': value,
            'tag_id': tag_id
        })


class AllTags(APIView):
    def post(self, req: Request):
        all_tags = Tag.objects.all()
        return_data = []
        for tag in all_tags:
            return_data.append({
                'tag_id': tag.id,
                'name': tag.name,
                'num': tag.num,
            })
        return Response({
            'all_tags': return_data
        })


class DeleteTag(APIView):
    def post(self, req: Request):
        tag_id = req.data['tag_id']
        value = -1
        try:
            Tag.objects.filter(id=tag_id).delete()
            value = 0
        except Exception as e:
            print(e)
            value = 1
        return Response({
            'value': value
        })


class GetTagDetail(APIView):
    def post(self, req: Request):
        tag_id = req.data['tag_id']
        value = -1
        name = ''
        num = 0
        try:
            tag = Tag.objects.get(id=tag_id)
            value = 0
            name = tag.name
            num = tag.num
        except Exception as e:
            print(e)
            value = 1
        return Response({
            'value': value,
            'name': name,
            'num': num,
        })
