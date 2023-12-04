<template>
    <v-container
    fluid
    >
        <v-tabs
        vertical
        >
              <!-- 展示所有帖子的内容 -->
      <div id="content" style="overflow:auto">
        <p class="title">我的帖子</p>
        <el-divider />
        <div class="common-list" >
          <div class="post-separator">
          <div class="common-wrap" v-for="item in posts" :key="item.post_id">
            <div class="common-item">
             <router-link :to="`/main/post/${item.post_id}`"
              type="primary"
              size="large"
              class="post-title" 
             >{{ item.title }}</router-link>
              <div class="post-content">
                <p class="post-info">帖子编号: {{ item.post_id }}</p>
                <p class="post-info">内容: {{ item.content }}</p>
                <p class="post-info">发布于: {{ item.data }}</p>
                
              </div>
              <div>
              <el-button 
              type="primary"
              size="large"
              @click="deleteP(item.post_id)">
                删除帖子
              </el-button>
            <el-button 
            type="primary"
            size="large"
            @click="showDialog1(item.post_id)">
                修改帖子
            </el-button>
            </div>
            </div>
            <Dialog
                :show="dialogConfig1.show"
                :title="dialogConfig1.title"
                :buttons="dialogConfig1.buttons"
                width="700px"
                :showCancel="false"
                @close="dialogConfig1.show = false"
                >
                <el-form
                    :model="formData1"
                    :rules="rules"
                    ref="formDataRef"
                    label-width="80px"
                    @submit.pervent
                >
                <el-form-item>
                <h2>修改帖子</h2>

                <el-form-item label="title">
                   <div class="modal-content">
                        <el-input
                        :rows="3"
                        
                        size="large"
                        placeholder="请输入标题"
                        v-model.trim="formData1.title"
                        ></el-input>
                   </div>
                </el-form-item>
                <el-form-item label="content">
                    <div class="modal-content">
                        <el-input
                        maxlength="300"
                        show-word-limit
                        style="width: 250px"
                        height="250px"
                        :rows="20"
                        
                        placeholder="请输入内容"
                        v-model.trim="formData1.content"
                        ></el-input>
                   </div>
                </el-form-item>
                </el-form-item>
                </el-form>
            </Dialog>
            </div>
              </div>
              </div>
              </div>
       
        </v-tabs>
    </v-container>

</template>

<script setup>

import {ref, reactive, getCurrentInstance, nextTick, onMounted } from "vue";
import {useRouter, useRoute} from "vue-router";
import {myPosts, getPost, deletePost, changePost} from '../../api/postFunc';
import Dialog from '../../components/Dialog.vue';
    
const { proxy } = getCurrentInstance();
const router = useRouter();
const route = useRoute();
const userMessage = ref({
    "username" : proxy.VueCookies.get("userInfo").name,
})
const posts = ref([]);
const myPostIds = ref([]);
const formData1 = ref({});

onMounted(()=>{
    initData();
})

const initData = async () => {
    var data = myPosts(userMessage.value.username);
    data.then((result) => {
        if (result.value != 0) {
            //proxy.Message.error("获取帖子失败");
        } else {
            myPostIds.value = result.post_ids;
            getContent();
        }
    })
}

const getContent = async ()=>{
    //console.log(myPostIds.value[0]);
    //console.log(myPostIds.value[1]);
    myPostIds.value.forEach(async (post_id)=> {
        //console.log(post_id);
        
        var result1 = await getPost(post_id);
        var params = {
          "post_id" : post_id,
          "title" : result1.title,
          "content" : result1.content,
          "data" : result1.data,
        };
        //console.log(params);
        posts.value.push(params);
        
    });
    
};


const showDialog1 = (post_id)=>{
        dialogConfig1.show = true;
        formData1.value.post_id = post_id;
};

const dialogConfig1 = reactive({
        show: false,
        title: "修改帖子",
        buttons: [
        {
        type: "primary",
        text: "提交",
        click: () => {
            submitPost();
            
          },
        },
        ],
    });

const submitPost = async () => {
    let params = {};
       
    Object.assign(params, formData1.value);
    params.username = userMessage.value.username;
    console.log(params.post_id);
    var value = changePost(params);
    value.then((result)=>{
        if (result.value == 0) {
        proxy.Message.success("修改成功");
        initData();
        router.go();
    } else{
        proxy.Message.error("修改错误");
        }
    });
};

    const deleteP = (post_id) => {
        var data = deletePost(post_id);
        data.then((result)=>{
          if (result == 0) {
            proxy.Message.success("删除帖子成功");
            initData();
            router.go();
          } else {
            proxy.Message.error("删除失败");
          }
        });
      
    }

</script>

<style lang="scss" scoped>

.title{
  font-size: 30px;
  margin-left: 20px;
  margin-top: 30px;
  font-weight: bolder;
}

.post-title {
    margin-bottom: 10px;
  font-size: 18px;
  font-weight: bold;
}

.post-content {
  /* Add styles for the content section */
  /* For example: */
  margin-top: 10px;
  font-size: larger;
  font-weight: bold;
  text-align: left;
}

  .post-separator {
    display: flex;
    flex-direction:row;
    flex-wrap:wrap;
    justify-content:left;
  }

  .post-info {
  margin-bottom: 5px;
  font-size: 14px;
  font-weight: bold;
  }
  
  .common-item{
  background-color: rgba(251, 247, 255, 0.8); 
  width: 330px;
  /* border: 15px solid rgba(214, 176, 255, 0.5); */
  padding: 20px;
  margin: 25px;
  border-radius: 20px;
  
  transition: all .3s ease-in 0s;
  -webkit-transition: all .3s;

  } 

  .common-item:hover{
    box-shadow: 10px 10px 5px #888888;
    transform: scale(1.2);
  }

</style>