<template>
    <div id="content" style="overflow:auto" >
        <div class="common-list" >
          <div class="common-wrap" v-for="item in commodities" :key="item.commodity_id">
            <div class="common-item">
              <div class="post-separator"></div>
             
              <div class="post-content">
                <p class="post-info">商品编号: {{ item.commodity_id }}</p>
                <p class="post-info">商品名：{{ item.name }}</p>
                <p class="post-info">描述 {{ item.dc }}</p>
                <p class="post-info">价格: {{ item.price }}</p>
                <p class="post-info">状态: {{ item.state == 0 ?"未出售":"已出售" }}</p>
                <!--显示状态-->
              </div>
              <div class="post-photos">
                <!--item.photos-->
                <img v-for="photo in commodities.photos" :src="photo.path"  :key="photo.photo_id" class="post-photo" />
              </div>


              <div v-if="post_user==userMessage.username">
                <!--添加照片-->
                <el-button
                type="primary"
                size="large"
                @click="dialogConfig.show = true">
                添加照片
                </el-button>
              
              <Dialog
              :show="dialogConfig.show"
              :title="dialogConfig.title"
              :buttons="dialogConfig.buttons"
              width="700px"
              :showCancel="true"
              @close="dialogConfig.show = false">

              <el-form
              :model="formData"
              ref="formDataRef"
              label-width="80px"
               @submit.prevent
              >
              <el-form-item label="照片" prop="">
                <div class="img-show">

                  <template v-if="localFile">
                   <img :src="localFile" />
                  </template>

                </div>
                <div class="select-btn">
                 <el-upload
                  name="file"
                  :show-file-list="false"
                   accept=".png,.PNG,.jpg,.JPG,.jpeg,.JPEG,.gif,.GIF,.bmp,.BMP"
                  :multiple="false"
                  :http-request="uploadImage">
    
                  <el-button type="primary">选择</el-button>
                   </el-upload>
                </div>
              </el-form-item>
              </el-form>

              </Dialog>
              </div>

              <div v-else >
                <el-button v-if="item.state == 0"
                type="primary"
                size="large"
                @click="buyCommodity(item.commodity_id)">
                购买
                </el-button>
              </div>
          </div>

          </div>
        </div>
      </div>


</template>

<script setup>
import {ref, reactive, getCurrentInstance, nextTick, onMounted } from "vue";
import {useRouter, useRoute} from "vue-router";

import Dialog from './Dialog.vue';
import { addCommodityPicture, createOrder } from '../api/postFunc';
const { proxy } = getCurrentInstance();

const router = useRouter();
const route = useRoute();

const props = defineProps({
    commodities: {
        type: Array,
    },
    post_id: {
        type: String,
    },
    post_user: {
      type: String,
    }

});

const userMessage = ref({
  "username": proxy.VueCookies.get("userInfo").name,
});

const localFile = ref(null);

const formData = ref({});
//photo:FILE, commodity_id:int

const dialogConfig = ref({
  show: false,
  title: "上传图片",
  buttons: [
    {
      type: "primary",
      text: "确定",
      click: (e) => {
        submitForm();
      },
    },
  ],
});


const submitForm= async ()=> {

    if (!(formData.value.photo instanceof File)) {
        dialogConfig.value.show = false;
        return;
    }
    
    let params = {
        "commodity_id" : formData.value.commodity_id,
        "photo" : formData.value.photo,
    };

    console.log(params.commodity_id);
    console.log(params.photo);
    var value;
    value = addCommodityPicture(params);
    value.then((result)=>{
        console.log(result);
        //value? 
        //photo_id?
        if (result.value == 0) {
          proxy.Message.success("添加照片成功");
        } else {
          proxy.Message.error("添加照片失败");
        }
        //photo_id
    })
    
    dialogConfig.value.show = false;
    //更改photo
    
};

const uploadImage = async (file) => {
  file = file.file;
  console.log(file);
  let img = new FileReader();
  img.readAsDataURL(file);
  console.log(img);
  img.onload= ({ target }) => {
    localFile.value = target.result;
  };
  
  //file 格式？
  formData.value.photo = file;
  console.log(formData.value.photo);
  //emit("update:modelValue", file);
};

const buyCommodity = (commodity_id)=>{
    var params = {
      "commodity_id" : commodity_id,
      "username" : userMessage.value.username,
    };
    var data = createOrder(params);
    data.then((result)=>{
      if(result.value == 0){
        proxy.Message.success("订单创建成功");
      } else {
        proxy.Message.error("订单创建失败");
      }
      //order_int
    });

};

</script>

<style>
.common-list {
  /* Add styles for the list container */
  /* For example: */
  margin: 0;
  padding: 0;
  
}

.common-wrap {
  /* Add styles for each item wrapper */
  /* For example: */
  margin-bottom: 10px;
  font-size: larger;
  text-align: left;
}

.common-item {
  /* Add styles for each item */
  /* For example: */
  border: 1px solid #ccc;
  padding: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.post-separator {
  /* Add styles for the separator */
  /* For example: */
  height: 1px;
  background-color: #ccc;
  margin: 10px 0;
}

.post-link {
  /* Add styles for the link */
  /* For example: */
  color: #007bff;
  text-decoration: none;
}

.post-content {
  /* Add styles for the content section */
  /* For example: */
  margin-top: 10px;
  font-size: larger;
  font-weight: bold;
  text-align: left;
}

.post-info {
  /* Add styles for the info paragraphs */
  /* For example: */
  margin-bottom: 5px;
  font-size: 14px;
  font-weight: bold;
}

.post-photos {
  display: flex;
  flex-wrap: wrap;
  margin-top: 10px;
}

.post-photo {
  width: 100px;
  height: 100px;
  object-fit: cover;
  margin-right: 10px;
  margin-bottom: 10px;
}

</style>