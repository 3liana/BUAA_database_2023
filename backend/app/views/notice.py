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


class AllNotice(APIView):
    def post(self):
        return_data = []
        try:
            notices = Notice.objects.all()
            for notice in notices:
                return_data.append({
                    'notice_id': notice.id,
                    'time': notice.time,
                    'title': notice.title,
                    'content': notice.content,
                    'username': notice.admin.username,
                })
        except Exception as e:
            print(e)
        return Response({
            'return_data': return_data
        })


# class ChangeNotice(APIView):
#     def post(self,req:Request):
#         notice_id = req.data['notice_id']
class DeleteNotice(APIView):
    def post(self, req: Request):
        notice_id = req.data['notice_id']
        try:
            Notice.objects.filter(id=notice_id).delete()
            value = 0
        except Exception as e:
            print(e)
            value = -1
        return Response({
            'value': value
        })
