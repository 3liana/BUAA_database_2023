from django.shortcuts import render
from rest_framework.views import APIView, Request
from rest_framework.response import Response

from app.models import *


class CreatePost(APIView):
    def post(self, req: Request):
        data = req.data
        username = data['username']
        title = data['title']
        content = data['content']
        post_id = -1
        value = -1
        try:
            user = User.objects.get(username=username)
            post = Post.objects.create(
                title=title,
                content=content,
                # user = user,
                user=user,
            )
            post_id = post.id
            post.save()
            value = 0
        except Exception as e:
            print(e)
            value = 1
        return Response({'value': value, 'post_id': post_id})


class DeletePost(APIView):
    def post(self, req: Request):
        post_id = req.data['post_id']
        value = 1
        try:
            Post.objects.get(id=post_id).delete()
            value = 0
        except Exception as e:
            print(e)
        return Response(value)


class GetPostCommodities(APIView):
    def get(self, req: Request):
        post_id = req.data['post_id']
        post = Post.objects.get(id=post_id)
        return_data = []
        commodities = Commodity.objects.filter(post=post)
        for item in commodities:
            return_data.append({
                'commodity_id': item.id,
                'name': item.name,
                'dc': item.description,
                'price': item.price,
            })
        return Response({'commodities': return_data})


class GetPost(APIView):
    def get(self, req: Request):
        post_id = req.data['post_id']
        post = Post.objects.get(id=post_id)  # 根据主键查找
        return Response({
            'title': post.title,
            'content': post.content,
            'user': post.user,
            'date': post.time
        })


class GetAllPosts(APIView):
    def post(self, req: Request):
        return_data = []
        allPost = Post.objects.all()
        for post in allPost:
            return_data.append({
                'post_id': post.id,
                'title': post.title,
                'content': post.content,
                'username': post.user.username,
                'date': post.time
            })
        return Response({
            "allposts": return_data
        })
