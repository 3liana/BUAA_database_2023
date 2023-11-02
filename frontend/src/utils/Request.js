import { ElLoading } from 'element-plus'
import router from '@/router'

import Message from '../utils/Message'

import axios from 'axios';

const contentTypeFrom = 'application/x-www-form-urlencoded;charset=UTF-8'
const contentTypeJson = 'application/json'
//arraybuffer ArrayBuffer对象
//blob Blob对突
const responseTypeJson = "json"
let loading = null;
const instance = axios.create({
    baseuRL: '/api',
    timeout: 10 * 1000,
});
//请求的栏截器
instance.interceptors.request.use(
    (config) => {
        if (config.showLoading) {
            loading = ElLoading.service({
                lock: true,
                text: '加载中......'
                //background: 'rgba(0, 0, 0, 0.7)',
            });
        }
        return config;
    },
    (error) =>{
        if (config.showLoading && loading) {
            loading.close();
        }
        Message.error("请求发送失败");
        return Promise.reject("请求发送失败");
    }
);
//请求后拦截器
instance.interceptors.response.use(
    (response) => {
        const { showLoading, errorCallback, showError = true, responseType } = response.config;
        if (showLoading && loading) {
            loading.close()
        }
        const responseData = response.data;
        if (responseType == "arraybuffer" || responseType == "blob") {
            //流的形式->无法解析，直接返回
            return responseData;
        }
        //正常请求
        if (responseData.code == 200) {
            //和后端匹配(后端返回)
            return responseData;
        } else if (responseData.code == 901) {
            //登录超时 跳到登录界面
            //?redirectUrl=" + encodeURI... ：记录当前页面路径，登录后还可以跳回
            router.push("/login?redirectUrl=" + encodeURI(router.currentRoute.value.path));
            return Promise.reject({ showError: false, msg: "登录超时"});
        } else {
            //其他错误
            if (errorCallback) {
                //如果存在错误信息的回调函数
                errorCallback(responseData.info);
            }
            return Promise.reject({ showError: showError, msg: responseData.info });

        }
    },
    (error) => {
        if (error.config.showLoading && loading) {
            loading.close();
        }
        return Promise.reject({ showError: true, msg: "网络异常"})
    }
);

const request = (config) => {
    const { url, params, dataType, showLoading = true, responseType = responseTypeJson } = config;//BUG???
    let contentType = contentTypeForm;
    let formData = new FormData();// 创建form对象
    for (let key in params) {
        formData.append(key, params[key] == undefined ? "" : params[key]);
    }
    if (dataType != null && dataType == 'json') {
        contentType = contentTypeJson;
    }
    let headers = {
        'Content-Type' : contentType,
        'X-Requested-with' : 'XMLHttpRequest',
    }

    return instance.post(url, formData, {
        onUploadProgress: (event) => {
            if (config.uploadProgressCallback) {
                //上传的时候回调上传函数
                config.uploadProgressCallback(event);
            }
        },
        responseType: responseType,
        headers: headers,
        showLoading: showLoading,
        errorCallback: config.errorCallback,
        showError: config.showError
    }).catch(error => {
        //console
        console.log(error);
        if (error.showError) {
            Message.error(error.msg);
        }
        return null;
    });
};

export default request;