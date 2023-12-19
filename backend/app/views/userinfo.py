from rest_framework.views import APIView, Request
from rest_framework.response import Response
from app.models import *


class GetInfo(APIView):
    def post(self, req: Request):
        data = req.data
        username = data['username']
        value = -1
        motto = ''
        average_score = 0
        comment_data = []
        try:
            user = User.objects.get(username=username)
            motto = user.motto
            comments = CommentOnPeople.objects.filter(to_user=user)
            count = 0
            for comment in comments:
                comment_data.append({
                    'from_user': comment.from_user.username,
                    'score': comment.score,
                    'txt': comment.txt,
                    'time': comment.time,
                })
                average_score += comment.score
                count += 1
            if not count == 0:
                print(average_score)
                print(count)
                average_score /= count
            value = 0
        except Exception as e:
            print(e)
            value = 1
        return Response({
            "value": value,
            "motto": motto,
            'comments': comment_data,
            'ave_score': average_score,
        })


class SetMotto(APIView):
    def post(self, req: Request):
        data = req.data
        motto = data['motto']
        username = data['username']
        value = -1
        try:
            user = User.objects.get(username=username)
            user.motto = motto
            user.save()
            value = 0
        except Exception as e:
            print(e)
            value = 1
        return Response({
            'value': value
        })
