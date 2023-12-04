<template>
    <div id="content" style="overflow:auto" >
        <div class="common-list" >
          <el-carousel type="card" height="350px" :autoplay="false">
            <el-carousel-item v-for="item in commodities" :key="item.commodity_id">
                <div class="post-content">
                  <p class="post-id">商品编号: {{ item.commodity_id }}</p>
                  <p class="post-title">{{ item.name }}</p>
                  <p class="post-info">描述: {{ item.dc }}</p>
                  <p class="post-info">价格: {{ item.price }}</p>
                  <p class="post-info">状态: {{ item.state == 0 ? "未出售":"已出售" }}</p>
                </div>

                <div class="post-photos">
                  <img v-for="photo in item.photos" :src="'data:image/jpeg;base64,' +photo.base64"  :key="photo.photo_id" class="post-photo" />
                </div>

                <div v-if="post_user==userMessage.username">
                  <el-button class="comButton"
                  type="primary"
                  size="large"
                  @click="addPicture(item.commodity_id)">
                  添加照片
                  </el-button>
                </div>

                <div v-else >
                  <el-button v-if="item.state == 0"
                  type="primary" class="comButton"
                  size="large"
                  @click="buyCommodity(item.commodity_id)">
                  购买
                  </el-button>
                </div>
            </el-carousel-item>
          </el-carousel>
              

              
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
              <el-form-item label="照片" prop="" >
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

const addPicture = (commodity_id)=>{
  dialogConfig.value.show = true;
  formData.value.commodity_id = commodity_id;

};

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
          router.go();
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
    console.log(localFile.value);
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
      if(result.value == 0) {
        proxy.Message.success("订单创建成功");
        router.push('/finished/buyer');
        //window.location.reload();
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

.post-title{
  text-align: center;
  font-size: 30px;
  text-decoration:overline;
  color: black;
}

.post-id{
  text-align: right;
  margin-right: 10px;
  font-size: 15px;
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
  margin-left: 20px;
  margin-bottom: 5px;
  font-size: 20px;
  font-weight: bold;
}

.post-photos {
  display: flex;
  flex-wrap: wrap;
  margin-top: 10px;
}

.post-photo {
  margin-left: 20px;
  width: 100px;
  height: 100px;
  object-fit: cover;
  margin-right: 10px;
  margin-bottom: 10px;
}

.comButton{
  margin-left: 250px;
  margin-bottom: 25px;
}

.el-carousel__item h3 {
  color: #475669;
  
  /* line-height: 200px; */
  margin: 0;
  text-align: center;
}

.el-carousel__item:nth-child(2n) {
  /*其他商品*/
  background-color: rgba(174, 147, 216, 0.8);
}

.el-carousel__item:nth-child(2n + 1) {
  /*正中商品*/ 
  background-color: rgba(221, 197, 255, 0.8);
}

</style>