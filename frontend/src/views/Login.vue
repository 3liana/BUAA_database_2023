<template>
    <div class="login-body">
        <div class="bg"></div>
        <div class="login-panel">
            <el-form
                class="login-register"
                :model="formData"
                :rules="rules"
                ref="formDataRef"
                
            >
            <div class="login-title">北航十三公寓二手市场</div>
            <!--input输入name-->
            <el-form-item prop="name">
                <el-input 
                size="large" 
                clearable 
                placeholder="请输入用户名" 
                v-model.trim="formData.name"
                maxLength="10"
                >
                <!--加窗口小图标-->
                <template #prefix>
                    <span class="iconfont icon-account"></span>
                </template>
                </el-input>
            </el-form-item>
            <!--登录密码-->
            <el-form-item prop="password">
                <el-input
                    type="password"
                    size="large"
                    placeholder="请输入密码"
                    v-model.trim="formData.password"
                    show-password
                    maxLength="20"
                    
                >
                <template #prefix>
                    <span class="iconfont icon-password"></span>
                </template>
                </el-input>
            </el-form-item>

            <!--注册新加-->
            <div v-if="opType == 0||opType == 2">
                <el-form-item prop="phone" v-if="opType==0">
                    <el-input
                        size="large"
                        placeholder="请输入手机号"
                        v-model.trim="formData.phone"
                        maxLength="20"
                    >
                    <template #prefix>
                    <span class="iconfont icon-account"></span>
                    </template>    
                </el-input>
                    
                </el-form-item>
                
                <el-form-item prop="wechat" v-if="opType==0">
                    <el-input
                        size="large"
                        placeholder="请输入微信号"
                        v-model.trim="formData.wechat"
                        maxLength="30"
                    >
                    <template #prefix>
                    <span class="iconfont icon-account"></span>
                    </template>    
                </el-input>
                    
                </el-form-item>

            </div>  
           

            <!--登录跳转按钮-->
            <el-form-item v-if="opType==1">
                <div class="rememberme-panel">
                    <el-checkbox v-model="formData.rememberme">记住我</el-checkbox>
                </div>
                <div class="no-account">
                    <!--bass.scss中加了a-link;忘记密码就重置所以传2,没有账号就注册所以传0-->
                    <a href="javascript:void(0)" class="a-link" @click="showPanel(2)">忘记密码?</a>
                    <a href="javascript:void(0)" class="a-link" @click="showPanel(0)">没有账号</a>
                </div>
            </el-form-item>

            <!--注册跳转按钮-->
            <el-form-item v-if="opType==0">
                <div class="no-account">
                    <a href="javascript:void(0)" class="a-link" @click="showPanel(1)">去登录</a>
                </div>
            </el-form-item>
            <!--登录\主策按钮-->
            <el-form-item prop="" v-if="opType==1">
                <el-button type="primary" class="op-btn" size="large" @click="doSubmit">
                    <span>登录</span>
                </el-button>
            </el-form-item>
            <el-form-item prop="" v-if="opType==0">
                <el-button type="primary" class="op-btn" size="large" @click="doSubmit">
                    <span>注册</span>
                </el-button>
            </el-form-item>
        </el-form>
        </div>
    </div>
</template>

<script setup>

    //import { url } from "inspector";
    import {ref, reactive, getCurrentInstance, nextTick, onMounted } from "vue";
    import {useRouter, useRoute} from "vue-router";
    import md5 from "js-md5";
    import { inviteUserIntoChatGroup , userLogin} from "../api/postFunc";

    const { proxy } = getCurrentInstance();

    const router = useRouter();
    const route = useRoute();
    //接口
    const api = {
        register:"/register/",
        login:"/login/",
    };

    //操作类型 0:注册 1:登录 2:重置密码

    const opType=ref(1);
    //重置表单
    const restForm = ()=>{
        formDataRef.value.resetFields();
        formData.value = {};
        if (opType.value==1) {
            //remember
            const cookieLoginInfo = proxy.VueCookies.get("loginInfo");
            if (cookieLoginInfo) {
                formData.value = cookieLoginInfo;
            }
        }
    };
    const showPanel = (type)=>{
        opType.value=type;
        //切换时清空表单
        restForm();
    };

    onMounted(()=>{
        showPanel(1);
    })

    const formData = ref({});
    const formDataRef = ref();
    
    const checkRePassWord = (rule, value, callback) => {
        if (value !== formData.value.password) {
            callback(new Error(rule.message));
        } else {
            callback();
        }
    };

    //prop:[] 添加约束
    const rules = {    
        title: [{ require: true, message: "请输入内容"}],
        password: [{require: true, message: "请输入密码"},
            {validtor:proxy.Verify.password, message:"密码只能是数字,字母,特殊字符,且要求8-18位"}],
        wechat: [{require: true, message: "请输入微信号"}],
        name: [{require: true, message: "请输入用户名"}],
        registerPassword: [
            {require: true, message: "请再次输入密码"},
            {validtor: checkRePassWord, message:"两次输入的密码不一致"}
        ],
    }; 

    // 登录、注册提交表单



    //后端一个接口checkCodeUrl
    //const checkCodeUrl=ref(api.checkCode);
    //const changeCheckCode = (type) =>{
    //    checkCodeUrl.value = api.checkCode + "?type=" + type + "&time=" + new Date().getTime(); 
        
    //};

    //检查数据正确性？？bug
    //登录、注册、提交表单


    const doSubmit=()=> {
        formDataRef.value.validate(async (valid)=> {
            if (!valid) {
                return;
            }
            let params = {};
            Object.assign(params, formData.value);
           
        
            //登录
            var value;
            if (opType.value==1) {
                //console.log("login");
                //console.log(params);
                let cookieLoginInfo = proxy.VueCookies.get("loginInfo");
                let cookiePassword = cookieLoginInfo==null ? null : cookieLoginInfo.password;
                /*if (params.password !== cookiePassword) {
                    //输入的密码不是从cookie中取的
                    params.password = md5(params.password);
                }*/
                console.log(params);
                value = userLogin(params);
                value.then((result) => {
                    console.log(result);
                    if (result.value == 0) {
                        proxy.Message.success("登录成功");
                        //存储Cookie
                        //登录成功
                        //type:0 普通用户， 1 管理员 
                       
                        formData.value.usertype = result.type;
                        console.log(formData.value.usertype);
                        proxy.VueCookies.set("userInfo", formData.value, 0);
                        console.log(proxy.VueCookies.get("userInfo").name);
                        //重定向到原始页面
                
                         const redirectUrl = route.query.redirectUrl||"/";
                        //console.log(redirectUrl);
                        router.push(redirectUrl);
                    } else if (result.value == 1) {
                        proxy.Message.error("用户名不存在");
                        return;
                    } else if (result.value == 2) {
                        proxy.Message.error("密码错误");
                        return;
                    } 
                    //result.type -> 用户类型
                })
            } else if (opType.value == 0) { 
                //console.log(params);
                value = inviteUserIntoChatGroup(params);
                value.then((result) => {
                    console.log(result);
                    if (result.value == 0) {
                        proxy.Message.success("注册成功，请登录");
                        showPanel(1);
                    } else if (result.value == 1) {
                        proxy.Message.error('不满足数据约束条件');
                        return;
                    } else if (result.value == 2) {
                        proxy.Message.error('此微信号已被注册');
                        return;
                    } else if (result.value == 3) {
                        proxy.Message.error('此用户名已被注册');
                        return;
                    }
                })
            }


            /*let result = await proxy.Request({
                url:url,
                params:params,
                errorCallback:()=> {
                   
                    //刷新验证码(无)
                },
            })
            if (!result) {
                
                return;
            }*/

            //注册返回
            if(opType.value==0) {
                
            } else if (opType.value==1) {
                
            } 
        });
       
    };



</script>

<style lang="scss" scoped>
.login-body{
    height: calc(100vh);
    background-size: cover;
    background: url("../assets/login_bg.jpg");
    display: flex;
    .bg {
        flex: 1;
        background-size: cover;
        background-position: center;
        background-size: 800px;
        background-repeat: no-repeat;
        background-image: url("../assets/login_img.png");
    }
    .login-panel {
        width: 430px;
        margin-right: 15%;
        margin-top: calc((100vh - 500px) / 2);
        .login-register {
            padding: 25px;
            background:#fff;
            border-radius: 5px;
            .login-title {
                text-align: center;
                font-size:18px;
                font-weight: bold;
                margin-bottom: 20px;
            }
            .send-emali-panel {
                display: flex;
                width: 100%;
                justify-content: space-between;
                .send-mail-btn {
                    margin-left: 5px;
                }
            }
            .rememberme-panel {
                width: 100%;
            }
            .no-account {
                width: 100%;
                display: flex;
                justify-content: space-between;
            }
            .op-btn {
                width: 100%;
            }
        }
    }
    .check-code-panel {
        width: 100%; 
        display: flex; 
        .check-code {
            margin-left: 5px;
            cursor: pointer;
        }
    }

    .login-btn-qq {
        margin-top:20px;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        img {
            cursor: pointer;
            margin-left: 10px;
            width: 20px;
        }
    }

}
</style>