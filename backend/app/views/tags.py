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
