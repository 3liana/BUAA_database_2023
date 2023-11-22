<template>
    <div>
        <el-form-item>
            <el-button
            type="primary"
            size="large"
            @click="showDialog">
                发布商品帖子
            </el-button>
            <Dialog
                :show="dialogConfig.show"
                :title="dialogConfig.title"
                :buttons="dialogConfig.buttons"
                width="700px"
                :showCancel="false"
                @close="dialogConfig.show = false"
                >
                <el-form
                    :model="formData"
                    :rules="rules"
                    ref="formDataRef"
                    label-width="80px"
                    @submit.pervent
                >
                <el-form-item>
                <h2>发布帖子</h2>
                <el-form-item label="title">
                   <div class="modal-content">
                        <el-input
                        :rows="3"
                        
                        size="large"
                        placeholder="请输入标题"
                        v-model.trim="formData.title"
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
                        v-model.trim="formData.content"
                        ></el-input>
                   </div>
                </el-form-item>
                </el-form-item>
                </el-form>
            </Dialog>
        </el-form-item>
      
      <!-- 展示所有帖子的内容 -->
      <div id="content" style="overflow:auto">
        <div class="common-list" v-infinite-scroll="load" infinite-scroll-disabled="disabled">
          <div class="common-wrap" v-for="item in allPosts" :key="item.post_id">
            <div class="common-item">
              <div class="post-separator"></div>
              
              <h3 class="post-title">标题: {{ item.title }}</h3>
              <div class="post-content">
                <p class="post-info">帖子编号: {{ item.post_id }}</p>
                <p class="post-info">作者: {{ item.user }}</p>
                <p class="post-info">内容: {{ item.content }}</p>
                <p class="post-info">发布于: {{ item.time }}</p>
            </div>
          </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
    import {ref, reactive, getCurrentInstance, nextTick, onMounted } from "vue";
    import {useRouter, useRoute} from "vue-router";
    import {createPost, getPost, getAllPosts} from '../../api/postFunc';
    import Dialog from '../../components/Dialog.vue';
    

    const { proxy } = getCurrentInstance();

    const router = useRouter();
    const route = useRoute();

    const formData = ref({});
    //const formDataRef = ref();

    const postIdCache = ref({
        //post_id:, 
    });

    const allPosts = ref([
      {
        post_id: 1,
        title: "test_title",
        content: "test_content",
        user: "test_user",
        data: "2023/11/22"
      },
    ]);
  
    const savePostIdCache = ()=> {
      localStorage.setItem('postIdCache', JSON.stringify(postIdCache.value));
    };

    const addPostId = (postId) => {
      postIdCache.value.push(postId);
      savePostIdCache();
    };

    const removePostId = (postId) => {
      const index = postIdCache.value.indexOf(postId);
      if (index > -1) {
        postIdCache.value.splice(index , 1);
        savePostIdCache();
      }
    };

    onMounted(() => {
      const cachedPostIds = localStorage.getItem('postIdCache');
      if (cachedPostIds) {
        postIdCache.value = JSON.parse(cachedPostIds);
      }
    });

    onMounted(() => {
      const initData = ()=>{
        var value = getAllPosts();
        value.then((result) => {
            allPosts.value = result.data; 
        })

        
      }

    });

    const getPostValue= (post_id) => {
      var value = getPost(post_id);
      value.then((result) => {
            console.log(result.value);
            if (result.value == 0) {
               allPosts.value.push({
                post_id: post_id,
                title: value.title,
                content: value.content,
               });
               
            } else {
                alert('fault in getPost');
            }
        });
      return value;
    };

    const dialogConfig = reactive({
        show: false,
        title: "发布帖子",
        buttons: [
        {
        type: "primary",
        text: "提交",
        click: () => {
            submitPost();
            console.log("submit!");
            },
        },
        ],
    });

    const showDialog = ()=> {
        dialogConfig.show = true;
    };
   
    const submitPost = () => {
        let params = {};
        Object.assign(params, formData.value);
        params.username = proxy.VueCookies.get("userInfo").name;
        //console.log(params.content);
	      console.log(params.title);
        var value = createPost(params);
        value.then((result) => {
            
            if (result.value == 0) {
              console.log(result.post_id);
              //存储post_id
              addPostId(result.post_id);
              proxy.Message.success("发布成功");
            } else {
              console.log("value error");
                alert('发布错误');
                return;
            }
        });

    };

    onMounted(() => {
      //执行挂载后需要做的事情


    });
    
 
  </script>
  
  <style>
  .post-title {
  font-size: 18px;
  font-weight: bold;
}

.post-content {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  padding: 10px;
  margin-top: 10px;
  border-radius: 4px;
}
  .post-separator {
  height: 1px;
  background-color: #ccc;
  margin: 10px 0;
  }

  .post-info {
  margin-bottom: 5px;
  }

  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .modal-content {
    background-color: white;
    padding: 100px;
    border-radius: 20px;
    width: 100%;
  height: 100%;
  }
  
  .submit-com {
    background-color: white;
    padding: 20px;
    border-radius: 20px;

  }

  
/*.el-input{
	width: 371px;
	height: 353px;
	background-color: white;
	--el-input-border-radius: Opx;
	--el-input-focus-border-color: #FF4400;
}*/

  button {
    margin-bottom: 50px;
  }



  .header {
  height: 130px;
  display: flex;
  justify-content: center;
  align-items: center;
  }

  .input-wrap {
    display: flex;
    border: solid #FF0036;
    border-width: 2px;
  }

    .el-input__inner {
      width:400px;
      border: none;
      border-radius: 0;
    }

    .el-input__inner::placeholder {
      color: rgb(250, 68, 108);
    }

    .el-button {
      width: 10vw;
      color: #fff;
      font-size: 1rem;
      border: none;
      border-radius: 0;
      background-color: #FF0036;
    }
  



  .banner-slider {
    margin-left: 22vw;
    margin-right: 22vw;
  }

  .el-carousel__container {
    height: 460px;
    cursor: pointer;
  }
  .el-carousel__item h3 {
  color: #475669;
  font-size: 18px;
  opacity: 0.75;
  line-height: 300px;
  margin: 0;
  }
  .el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
  }
  .el-carousel__item:nth-child(2n+1) {
    background-color: #d3dce6;
  }

  .hot-list {
    display: flex;
    flex-wrap: wrap;
    float: left;
    margin: 50px 22vw 80px;
  }

      .hot-item-tag {
        height: 20px;
        visibility: hidden;
      }

      .hot-item-img {
        width: 185px;
        height: 185px;
      }

      .hot-item-title {
        margin: 8px auto;
        width: 135px;
        height: 40px;
        color: #333;
        font-size: 14px;

        overflow : hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp:2;
      }

      .hot-item-price {
        color:#FF0036;
        font-size: 18px;
        margin: 5px auto;
      }
    
    .hot-wrap:hover {
      border: 1px solid #FF0036;
    }
  

  .common-list {
    clear: both;
    margin-left: 22vw;
    margin-right: 22vw;
   
  }
  .common-wrap {
      margin-left: 22px;
    }

  </style>
  