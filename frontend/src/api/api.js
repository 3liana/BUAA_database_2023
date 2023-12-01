import axios from 'axios';
import { ElMessage } from 'element-plus';



export function post(url, data) {
    return new Promise((resolve,reject)=>{
        axios.post('http://127.0.0.1:8000'+url, data).then(response=>
        {resolve(response.data)}).catch((error)=>{
            ElMessage({
                message: "1网络连接失败",
                    grouping: true,
                    type: 'error',
            });
        });
    });
}

export function get(url){
    return new Promise((resolve,reject)=>{
        axios.get('http://127.0.0.1:8000'+url).then(response=>
            {resolve(response.data)}).catch((error)=>{
                ElMessage({
                    message: "网络连接失败",
                    grouping: true,
                    type: 'error',
                });
            });
    });
}