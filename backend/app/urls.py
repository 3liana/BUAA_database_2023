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
from app.views import comments
from app.views import userinfo

router = DefaultRouter()
# /user/由UserViewSet去处理
router.register(prefix='user', viewset=view_set.UserViewSet)

urlpatterns = [
                  # path('demo/', User.Demo.as_view()),
                  path('', include(router.urls)),
                  # 关于账号的功能
                  path('register', account.Register.as_view()),
                  path('login', account.Login.as_view()),
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
                  path('allUsers', account.AllUsers.as_view()),
                  path('setAvatorAdmin', account.SetAvatorAdmin.as_view()),
                  path('getAvatorAdmin', account.GetAvatorAdmin.as_view()),
                  # 关于帖子的功能
                  path('createPost', posts.CreatePost.as_view()),
                  path('deletePost', posts.DeletePost.as_view()),
                  path('getPostCommodities', posts.GetPostCommodities.as_view()),
                  path('getPost', posts.GetPost.as_view()),
                  path('getAllPosts', posts.GetAllPosts.as_view()),
                  path('getPostTags', posts.GetPostTags.as_view()),
                  path('addTagToPost', posts.AddTagToPost.as_view()),
                  path('deleteTagToPost', posts.DeleteTagToPost.as_view()),
                  path('deletePost', posts.DeletePost.as_view()),
                  path('changePost', posts.ChangePost.as_view()),
                  path('getUser', posts.GetUser.as_view()),
                  path('getPostsWithTag', posts.GetPostsWithTag.as_view()),
                  # 关于商品的功能
                  path('createCommodity', commodities.CreateCommodity.as_view()),
                  path('getCommodityPictures', commodities.GetCommodityPictures.as_view()),
                  path('addCommodityPicture', commodities.AddCommodityPicture.as_view()),
                  path('checkIfOrdered', commodities.CheckIfOrdered.as_view()),
                  path('belongToPost', commodities.BelongToPost.as_view()),
                  path('getCommodityDetail', commodities.GetCommodityDetail.as_view()),
                  # 关于订单的功能
                  path('createOrder', orders.CreateOrder.as_view()),
                  path('cancelOrder', orders.CancelOrder.as_view()),
                  path('getOrder', orders.GetOrder.as_view()),
                  # 订单 新功能
                  path('checkStatus', orders.CheckStatus.as_view()),
                  path('status0_1', orders.Status0_1.as_view()),
                  path('status1_2', orders.Status1_2.as_view()),
                  path('commentOnPeople', orders.MakeCommentOnPeople.as_view()),
                  # 关于标签的功能
                  path('createTag', tags.CreateTag.as_view()),
                  path('allTags', tags.AllTags.as_view()),
                  path('deleteTag', tags.DeleteTag.as_view()),
                  path('getTagDetail', tags.GetTagDetail.as_view()),
                  # 关于公告的功能
                  path('createNotice', notice.CreateNotice.as_view()),
                  path('allNotice', notice.AllNotice.as_view()),
                  path('deleteNotice', notice.DeleteNotice.as_view()),
                  # 关于评论的功能
                  path('commentToPost', comments.CommentToPost.as_view()),
                  path('commentToComment', comments.CommentToComment.as_view()),
                  path('getPostFirstComments', comments.GetPostFirstComments.as_view()),
                  path('getFirstCommentsSecondComments', comments.GetFirstCommentsSecondComments.as_view()),
                  path('deleteFirstCommen', comments.DeleteFirstComment.as_view()),
                  path('deleteSecondComment', comments.DeleteSecondComment.as_view()),
                  # 关于个人信息的功能
                  path('setMotto', userinfo.SetMotto.as_view()),
                  path('getInfo', userinfo.GetInfo.as_view()),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
