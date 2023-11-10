from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import account
from app.views import view_set
from django.conf.urls.static import static
from django.conf import settings
from app.views import posts

router = DefaultRouter()
# /user/由UserViewSet去处理
router.register(prefix='user', viewset=view_set.UserViewSet)

urlpatterns = [
                  # path('demo/', User.Demo.as_view()),
                  path('', include(router.urls)),
                  # 关于账号的功能
                  path('register/', account.Register.as_view()),
                  path('login/', account.Login.as_view()),
                  path('setAvator', account.SetAvator.as_view()),
                  path('getAvator', account.GetAvator.as_view()),
                  path('myPosts', account.MyPosts.as_view()),
                  path('myOrdersAsSaler', account.MyOrdersAsSaler.as_view()),
                  path('myOrdersAsBuyer', account.MyOrdersAsBuyer.as_view()),
                  # 关于帖子的功能
                  path('createPost', posts.CreatePost.as_view()),
                  path('deletePost', posts.DeletePost.as_view()),
                  path('getPostCommodities', posts.GetPostCommodities.as_view()),
                  path('getPost', posts.GetPost.as_view()),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
