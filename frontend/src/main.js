import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'

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
import Confirm from '@/utils/Confirm'

loadFonts()

const app = createApp(App)

app.use(ElementPlus)
app.use(router)
app.use(vuetify)

app.config.globalProperties.Verify = Verify;
app.config.globalProperties.Message = Message;
app.config.globalProperties.Request = Request;
app.config.globalProperties.VueCookies = VueCookies;
app.config.globalProperties.Confirm = Confirm;



app.mount('#app')
