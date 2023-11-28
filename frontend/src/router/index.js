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
          path: '/myshare',
          name: '我发布的订单',
          meta: {
            needLogin: true,
            menuCode: "share"
          },
          component: () => import("@/views/share/MyOrderView.vue")
        },
        {
          path: '/finished',
          name: '已完成的订单',
          meta: {
            needLogin: true,
            menuCode: "finished"
          },
          component: () => import("@/views/finished/Finished.vue")
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
          path: '/settings/fileList',
          name: '用户文件',
          meta: {
            needLogin: true,
            menuCode: "settings"
          },
          component: () => import("@/views/admin/FileList.vue")
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
