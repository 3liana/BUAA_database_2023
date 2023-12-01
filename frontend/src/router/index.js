import { createRouter, createWebHistory } from 'vue-router'
import VueCookies from 'vue-cookies'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: '登录',
      component: ()=> import("@/views/Login.vue")
    },
    {
      path: '/',
      name: 'Framework',
      component: ()=> import("@/views/Framework.vue"),
      children:[
        {
          path: '/',
          redirect: '/main/post'
        },
        {
          path:'/main/post',
          name: '首页',
          meta: {
            needLogin: true,
            menuCode: "main"
          },
          component: () => import("@/views/main/Main.vue")
        },
        {
          path: '/main/post/:post_id(\\d+)',
          name: '帖子详情',
          props: true,
          meta:{
            needLogin: true,
            menuCode: "main",
            title: "求物",
            type: "buy"
          },
          component: () => import("@/views/main/PostDetailView.vue")
        },
        {
          path: '/main/notice',
          name: '公告栏',
          meta: {
            needLogin: true,
            menuCode: "main"
          },
          component: () => import("@/views/main/Notice.vue")
        },
        {
          path: '/myshare',
          name: '我的帖子',
          meta: {
            needLogin: true,
            menuCode: "share"
          },
          component: () => import("@/views/share/MyPostView.vue")
        },
        {
          path: '/finished/buyer',
          name: '我作为买家的订单',
          meta: {
            needLogin: true,
            menuCode: "finished"
          },
          component: () => import("@/views/finished/BuyOrder.vue")
        },
        {
          path: '/finished/seller',
          name: '我作为卖家的订单',
          meta: {
            needLogin: true,
            menuCode: "finished"
          },
          component: () => import("@/views/finished/SellOrder.vue")
        },
        {
          path: '/settings/sysSetting',
          name: '系统设置',
          meta: {
            needLogin: true,
            menuCode: "settings"
          },
          component: () => import("@/views/admin/SysSettings.vue")
        },
        {
          path: '/settings/userList',
          name: '用户管理',
          meta: {
            needLogin: true,
            menuCode: "settings"
          },
          component: () => import("@/views/admin/UserList.vue")
        },
        {
          path: '/settings/tagList',
          name: '系统文件',
          meta: {
            needLogin: true,
            menuCode: "settings"
          },
          component: () => import("@/views/admin/TagList.vue")
        },

      ]
    },
   
    
    

  ]
})

router.beforeEach((to, from, next)=>{
  const userInfo = VueCookies.get("userInfo")
  if (to.meta.needLogin != null && to.meta.needLogin && userInfo == null) {
    router.push("/login");
  }
  next();
})

export default router
