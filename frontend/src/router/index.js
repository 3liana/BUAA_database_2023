import { createRouter, createWebHistory } from 'vue-router'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Layout',
      component: ()=> import("@/views/Layout.vue")
    },
    {
      path: '/login',
      name: 'Login',
      component: ()=> import("@/views/Login.vue")
    },


  ]
})

export default router
