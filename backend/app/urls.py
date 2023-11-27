from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import account
from app.views import view_set
from django.conf.urls.static import static
from django.conf import settings
from app.views import posts
from app.views import commodities
from app.views import orders
from app.views import tags
from app.views import notice

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
                  path('getPassword', account.GetPassword.as_view()),
                  path('changePassword', account.ChangePassword.as_view()),
                  path('getUserInfo', account.GetUserInfo.as_view()),
                  path('banAUser', account.BanAUser.as_view()),
                  path('checkBan', account.CheckBan.as_view()),
                  # 关于帖子的功能
                  path('createPost', posts.CreatePost.as_view()),
                  path('deletePost', posts.DeletePost.as_view()),
                  path('getPostCommodities', posts.GetPostCommodities.as_view()),
                  path('getPost', posts.GetPost.as_view()),
                  path('getAllPosts', posts.GetAllPosts.as_view()),
                  path('getPostTags', posts.GetPostTags.as_view()),
                  path('addTagToPost', posts.AddTagToPost.as_view()),
                  path('deletePost', posts.DeletePost.as_view()),
                  path('changePost', posts.ChangePost.as_view()),
                  path('getUser', posts.GetUser.as_view()),
                  # 关于商品的功能
                  path('createCommodity', commodities.CreateCommodity.as_view()),
                  path('getCommodityPictures', commodities.GetCommodityPictures.as_view()),
                  path('addCommodityPicture', commodities.AddCommodityPicture.as_view()),
                  path('checkIfOrdered', commodities.CheckIfOrdered.as_view()),
                  # 关于订单的功能
                  path('createOrder', orders.CreateOrder.as_view()),
                  path('cancelOrder', orders.CancelOrder.as_view()),
                  path('getOrder', orders.GetOrder.as_view()),
                  # 关于标签的功能
                  path('createTag', tags.CreateTag.as_view()),
                  path('allTags', tags.AllTags.as_view()),
                  path('deleteTag', tags.DeleteTag.as_view()),
                  # 关于公告的功能
                  path('createNotice', notice.CreateNotice.as_view())
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
