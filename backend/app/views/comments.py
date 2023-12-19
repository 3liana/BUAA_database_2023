from rest_framework.views import APIView, Request
from rest_framework.response import Response
from app.models import *


class CommentToPost(APIView):
    def post(self, req: Request):
        data = req.data
        username = data['username']
        post_id = data['post_id']
        content = data['content']
        value = -1
        comment_id = -1
        try:
            user = User.objects.get(username=username)
            post = Post.objects.get(id=post_id)
            comment = FirstComment.objects.create(
                fromUser=user,
                post=post,
                content=content
            )
            comment_id = comment.id
            value = 0
        except Exception as e:
            print(e)
            value = 1
        return Response({
            'value': value,
            'comment_id': comment_id
        })


class CommentToComment(APIView):
    def post(self, req: Request):
        data = req.data
        username = data['username']
        comment_id = data['comment_id']
        content = data['content']
        value = -1
        comment_id2 = -1
        try:
            user = User.objects.get(username=username)
            first_comment = FirstComment.objects.get(id=comment_id)
            second_comment = SecondComment.objects.create(
                fromUser=user,
                toComment_id=comment_id,
                content=content
            )
            comment_id2 = second_comment.id
            value = 0
        except Exception as e:
            print(e)
            value = 1
        return Response({
            'value': value,
            'comment_id2': comment_id2
        })


class GetPostFirstComments(APIView):
    def post(self, req: Request):
        post_id = req.data['post_id']
        comments = FirstComment.objects.filter(post_id=post_id)
        return_data = []
        for comment in comments:
            return_data.append({
                'comment_id': comment.id,
                'from_user': comment.fromUser.username,
                'time': comment.time,
                'content': comment.content
            })
        return Response({
            'return_data': return_data
        })


class GetFirstCommentsSecondComments(APIView):
    def post(self, req: Request):
        comment_id = req.data['comment_id']
        comments2 = SecondComment.objects.filter(toComment_id=comment_id)
        return_data = []
        for comment in comments2:
            return_data.append({
                'comment_id2': comment.id,
                'from_user': comment.fromUser.username,
                'time': comment.time,
                'content': comment.content
            })
        return Response({
            'return_data': return_data
        })


class DeleteFirstComment(APIView):
    def post(self, req: Request):
        comment_id = req.data['comment_id']
        value = -1
        try:
            FirstComment.objects.get(id=comment_id).delete()
            value = 0
        except Exception as e:
            print(e)
            value = 1
        return Response({
            'value': value
        })


class DeleteSecondComment(APIView):
    def post(self, req: Request):
        comment_id2 = req.data['comment_id2']
        value = -1
        try:
            SecondComment.objects.get(id=comment_id2).delete()
            value = 0
        except Exception as e:
            print(e)
            value = 1
        return Response({
            'value': value
        })
