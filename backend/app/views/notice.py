from django.shortcuts import render
from rest_framework.views import APIView, Request
from rest_framework.response import Response

from app.models import *


class CreateNotice(APIView):
    def post(self, req: Request):
        data = req.data
        username = data['username']
        title = data['title']
        content = data['content']
        notice_id = -1
        value = -1
        try:
            admin = Administrator.objects.get(username=username)
            nocice = Notice.objects.create(
                title=title,
                content=content,
                admin=admin,
            )
            notice_id = nocice.id
            nocice.save()
            value = 0
        except Exception as e:
            print(e)
            value = 1
        return Response({'value': value, 'notice_id': notice_id})