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


class GetUser(APIView):
    def post(self, req: Request):
        post_id = req.data['post_id']
        username = ''
        value = -1
        try:
            username = Post.objects.get(id=post_id).user.username
            value = 0
        except Exception as e:
            print(e)
            value = -1
        return Response({
            'value': value,
            'username': username
        })


class GetPostCommodities(APIView):
    def post(self, req: Request):
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
    def post(self, req: Request):
        post_id = req.data['post_id']
        post = Post.objects.get(id=post_id)  # 根据主键查找
        return Response({
            'title': post.title,
            'content': post.content,
            'username': post.user.username,
            'date': post.time
        })
    def get(self, req: Request):
        post_id = req.query_params.get('post_id')
        if not post_id:
            return Response({"error": "No post_id provided"}, status=400)

        post = Post.objects.get(id=post_id)  # 根据主键查找
        return Response({
            'title': post.title,
            'content': post.content,
            'username': post.user.username,
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


class GetPostTags(APIView):
    def post(self, req: Request):
        post_id = req.data['post_id']
        tag_ids = []
        value = -1
        try:
            post_tags = Tag_Post.objects.filter(post__id=post_id)
            for post_tag in post_tags:
                tag_ids.append(post_tag.tag.id)
            value = 0
        except Exception as e:
            print(e)
            value = 1
        return Response({
            'value': value,
            'tag_ids': tag_ids,
        })


class DeleteTagToPost(APIView):
    def post(self, req: Request):
        data = req.data
        post_id = data['post_id']
        tag_id = data['tag_id']
        value = -1
        try:
            tag = Tag.objects.get(id=tag_id)
            Tag_Post.objects.filter(post__id=post_id, tag__id=tag_id).delete()
            tag.num = tag.num - 1
            tag.save()
            value = 0
        except Exception as e:
            print(e)
            value = 1
        return Response({
            'value': value
        })


class ChangePost(APIView):
    def post(self, req: Request):
        data = req.data
        post_id = data['post_id']
        title = data['title']
        content = data['content']
        value = -1
        try:
            post = Post.objects.get(id=post_id)
            if title != '':
                post.title = title
            if content != '':
                post.content = content
            post.save()
            value = 0
        except Exception as e:
            print(e)
            value = -1
        return Response({
            'value': value
        })


class AddTagToPost(APIView):
    def post(self, req: Request):
        data = req.data
        post_id = data['post_id']
        tag_id = data['tag_id']
        value = -1
        find = True
        try:
            item = Tag_Post.objects.get(post__id=post_id, tag__id=tag_id)
        except Tag_Post.DoesNotExist:
            find = False
        if(not find):
            try:
                tag = Tag.objects.get(id=tag_id)
                Tag_Post.objects.create(
                    post=Post.objects.get(id=post_id),
                    tag=tag,
                )
                tag.num = tag.num + 1
                tag.save()
                value = 0
            except Exception as e:
                print(e)
                value = 1
        else:
            value = 2
        return Response({
            'value': value
        })
