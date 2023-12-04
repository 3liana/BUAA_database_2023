<template>
    <div>
        <el-form-item>
            <el-button
            v-if="userMessage.usertype==1"
            type="primary"
            size="large"
            @click="showDialog">
                发布公告
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
                    
                    label-width="80px"
                    @submit.pervent
                >
                <el-form-item>
                <h2>发布公告</h2>
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
    </div>
     <!-- 展示所有公告的内容 -->


     <div id="content" style="overflow:auto">
        <div class="common-list" >
          <div class="common-wrap" v-for="item in allNotices">
            
            <el-card class="box-card">
                <template #header>
                <div class="card-header">
                    <span class="post_title">{{item.title }}</span>
                    <el-button class="button" text>公告编号：{{ item.notice_id }}</el-button>
                </div>
                </template>
                <p class="post-info">内容: {{ item.content }}</p>
                <template #footer>
                    <p>发布人: {{ item.username }}</p> 
                    <p>发布于: {{ item.time }}</p>

                    <div v-if="userMessage.usertype==1">
                <el-button class="deleteButton"
                @click="deleteThisNotice(item.notice_id)">
                    删除公告
                </el-button>
            </div>
                </template>
            </el-card>

        </div>
     </div>

    </div>

     <!-- <div id="content" style="overflow:auto">
        <div class="common-list" >
          <div class="common-wrap" v-for="item in allNotices">
            <div class="common-item">
              <div class="post-separator"></div>
              <div class="post-content">
                <p class="post-info"> 公告编号：{{ item.notice_id }}</p>
                <p class="post-title">公告标题：{{item.title }}</p>
                <p class="post-info">内容: {{ item.content }}</p>
                 <p class="post-info">发布人: {{ item.username }}</p> 
                <p class="post-info">发布于: {{ item.time }}</p>
                
              </div>
              <div v-if="userMessage.usertype==1">
                <el-button @click="deleteThisNotice(item.notice_id)">
                    删除公告
                </el-button>
            </div>
            </div>
            
        </div>
     </div>

    </div> -->
</template>

<script setup>
    import {ref, reactive, getCurrentInstance, nextTick, onMounted } from "vue";
    import {useRouter, useRoute} from "vue-router";
    import {createNotice, allNotice, deleteNotice } from '../../api/postFunc';
    import Dialog from '../../components/Dialog.vue';
    

    const { proxy } = getCurrentInstance();

    const router = useRouter();
    const route = useRoute();

    const formData = ref({});

    const allNotices = ref([
        /*
        {
        'time':str,
        'title': str,
        'content':str,
        'username': str,
        }
        */ 
    ]);

    const userMessage = ref({
        "username" : proxy.VueCookies.get("userInfo").name,
        "usertype" : proxy.VueCookies.get("userInfo").usertype,
    })

    onMounted(() => {
        //执行挂载后需要做的事情
        initData();

    });

    const initData = ()=>{
        console.log(userMessage.value.usertype);
        //getAllNotice
        var data = allNotice();
        data.then((result)=>{
            if (result.value == 0) {
                proxy.Message.error("获取公告失败");
            } else {
                Object.assign(allNotices.value, result.return_data);
            }
            
        });
    };

    const dialogConfig = reactive({
        show: false,
        title: "发布公告",
        buttons: [
        {
        type: "primary",
        text: "提交",
        click: () => {
            submitNotice();
           
          },
        },
        ],
    });

    const showDialog = ()=> {
        dialogConfig.show = true;
    };

    const submitNotice = ()=>{
        var params = {
            "username" : userMessage.value.username,
            "title" :formData.value.title,
            "content" : formData.value.content,
        };
        console.log(params);
        var data = createNotice(params);
        data.then((result) => {
            if (result.value == 0) {
                proxy.Message.success("发布公告成功");
                router.go();
            } else {
                proxy.Message.error("发布公告失败");
            }
        });
    };

const deleteThisNotice = (notice_id) => {
    var data = deleteNotice(notice_id);
    data.then((result)=>{
        if (result.value == 0) {
            proxy.Message.success("删除公告成功");
            router.go();
        } else {
            proxy.Message.error("删除失败");
        }
    });
};

const activeNames = ref(['1'])

</script>
    
<style>
 .post_title {

  font-size: 25px;
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

  .common-wrap {
      margin-left: 22px;
    }

    .card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}

.box-card {
    margin-top: 20px;
  width: 700px;
  background-color:antiquewhite;
  margin-left: 300px;
}
.deleteButton{
    margin-left: 550px;
}

</style>