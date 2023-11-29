<template>
    <div>
        <el-form-item>
            <el-button
            color="#626aef"
            size="large"
            @click="showDialog">
                发布帖子
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
                
                <el-form-item>
                  <!--展示所有tag-->
                  <div v-for="tag in tags">
                    <button @click=""></button>
                  </div>

                </el-form-item>
                </el-form-item>
                </el-form>
            </Dialog>
        </el-form-item>
      
      <!-- 展示所有帖子的内容 -->
      <div id="content" style="overflow:auto">
        <div class="common-list" >
          <div class="seperate">
          <div class="common-wrap" v-for="item in allPosts" :key="item.post_id">
            
            <div class="common-item">
              
             <router-link :to="`/main/post/${item.post_id}`"
              type="primary"
              size="large"
              class="post-title" 
             >{{ item.title }}</router-link>
              <div class="post-content">
                <p class="post-info">帖子编号: {{ item.post_id }}</p>
                <p class="post-info">发布者: {{ item.username }}</p>
                <p class="post-info">内容: {{ item.content }}</p>
                <p class="post-info">发布于: {{ item.data }}</p>             
              </div>
            <div v-if="item.username == userMessage.username">
              <br>
              <p class="tips">这是你发布的贴子，你可以对其进行以下修改： </p>
              <el-button plain
              color="#626aef"
              @click="deleteP(item.post_id)">
                删除帖子
              </el-button>

            <el-button 
            color="#626aef"
            plain
            @click="showDialog1">
                修改帖子
            </el-button>
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
                <h2>修改帖子{{ formData1.post_id = item.post_id }}</h2>

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
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
    import {ref, reactive, getCurrentInstance, nextTick, onMounted } from "vue";
    import {useRouter, useRoute} from "vue-router";
    import {createPost, getPost, getAllPosts, deletePost, changePost, allTags} from '../../api/postFunc';
    import Dialog from '../../components/Dialog.vue';
    

    const { proxy } = getCurrentInstance();

    const router = useRouter();
    const route = useRoute();

    const formData = ref({});

    const formData1 = ref({});
    //const formDataRef = ref();

    const postIdCache = ref({
        //post_id:, 
    });


    const allPosts = ref([
      {
        post_id: 1,
        title: "qwp",
        content: "test_content",
        user: "test_user",
        data: "2023/11/22"
      },
      {
        post_id: 2,
        title: "test_title2",
        content: "test_content2",
        user: "test_user2",
        data: "2023/11/27"
      },
      {
        post_id: 3,
        title: "test_title3",
        content: "test_content3",
        user: "test_user3",
        data: "2023/11/27"
      },
    ]);

    const tags = ref([
      {
        "tag_id" : 1,
        "name" : "零食",
        "num" : 2,
      },
      {
        "tag_id" : 2,
        "name" : "化妆品",
        "num" : 3,
      },
      
    ]);

    const userMessage = ref({
      "username":proxy.VueCookies.get("userInfo").name
    });
  
    const savePostIdCache = ()=> {
      localStorage.setItem('postIdCache', JSON.stringify(postIdCache.value));
    };

    const addPostId = (postId) => {
      postIdCache.push(postId);
      savePostIdCache();
    };

    const removePostId = (postId) => {
      const index = postIdCache.value.indexOf(postId);
      if (index > -1) {
        postIdCache.value.splice(index , 1);
        savePostIdCache();
      }
    };

    const initData = async()=>{
        console.log("init!");
        var value = getAllPosts();
        value.then((result) => {
            allPosts.value = result.allposts; 
            console.log(allPosts.value[0].post_id);
        })
    };


    onMounted(() => {
      //执行挂载后需要做的事情
      const cachedPostIds = localStorage.getItem('postIdCache');
      if (cachedPostIds) {
        postIdCache.value = JSON.parse(cachedPostIds);
      }
      initData();
    });

    

    const dialogConfig = reactive({
        show: false,
        title: "发布帖子",
        buttons: [
        {
        type: "primary",
        text: "提交",
        click: () => {
            submitPost(0);
            console.log("submit!");
            },
        },
        ],
    });

    const dialogConfig1 = reactive({
        show: false,
        title: "修改帖子",
        buttons: [
        {
        type: "primary",
        text: "提交",
        click: () => {
            submitPost(1);
            
          },
        },
        ],
    });

    const showDialog = ()=> {
        dialogConfig.show = true;
    };

    const showDialog1 = ()=>{
        dialogConfig1.show = true;
    }
   
    const submitPost = (type) => {
        let params = {};
        if (type == 0) {
        Object.assign(params, formData.value);
        params.username = userMessage.value.username;
        //console.log(params.content);
	      console.log(params.title);
        var value = createPost(params);
        value.then((result) => {
            
            if (result.value == 0) {
              console.log(result.post_id);
              //存储post_id
              //addPostId(result.post_id);
              proxy.Message.success("发布成功");
              initData();
              router.go();
            } else {
              proxy.Message.error("发布错误");
              return;
            }
        });
      } else {
        Object.assign(params, formData1.value);
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
      }
      
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
  
<style>
.post-title {
  margin-bottom: 10px;
  font-size: 22px;
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
  height: 1px;
  background-color: #ccc;
  margin: 10px 0;
  }

  .post-info {
  margin-bottom: 5px;
  font-size: 14px;
  font-weight: bold;

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

  /* button {
    margin-bottom: 50px;
  } */



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

    /* .el-button :hover{
       /* width: 10vw; */
      /*color: #fff;
      font-size: 1rem;
      border: none;
      border-radius: 50; 
      
    } */

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

    .seperate{
      display: flex;
      flex-direction:row;
      flex-wrap:wrap;
      justify-content:left;
      
    }
  

  /* .common-list {
    clear: both;
  } */

   .common-wrap {
    background-color: rgba(235, 216, 255, 0.5);
    width: 500px;
    border: 15px solid rgba(214, 176, 255, 0.5);
    padding: 15px;
    margin: 25px;
    box-shadow: 10px 10px 5px #888888;
    
      
    } 

  </style>
  