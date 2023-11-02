import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

//引入element plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
//
import '@/assets/icon/iconfont.css'
import '@/assets/base.scss'
//cookie
import VueCookies from 'vue-cookies'

import Verify from '@/utils/Verify'

import Message from '@/utils/Message'
import Request from '@/utils/Request'

//自定义组件(暂无)
//import Dialog from '@/components/Dialog.vue'


const app = createApp(App)
app.use(ElementPlus)
app.use(router)

//配置全局组件
app.config.globalProperties.Verify = Verify;
app.config.globalProperties.Message = Message;
app.config.globalProperties.Request = Request;
app.mount('#app')
