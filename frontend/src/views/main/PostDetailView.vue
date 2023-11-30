<template>

    <div class="container" fluid>
        
        <div class="card"  style="margin-top: 20px;">
          <p>帖子详情：</p>
          <div class="post-content">
                <p class="post-info">帖子编号: {{ postCache.post_id }}</p>
                <p class="post-info">作者: {{ postCache.username }}</p>
                <p class="post-info">内容: {{ postCache.content }}</p>
                <p class="post-info">发布于: {{ postCache.data }}</p>
                <p class="post-info"> tags: </p>
                <div class="tag" v-for="tag in postTags" :key="tag.tag_id">
                  <button @click="deleteTag(tag.tag_id)">
                    {{ tag.name }}
                  </button>
                </div>
          </div>

          <el-form-item v-if="postCache.username==userMessage.username">
            <el-button
              type="primary"
              size="large"
              @click="showDialog1">
              添加tag
            </el-button>
            <Dialog
            :show="dialogConfig1.show"
            :title="dialogConfig1.title"
            :buttons="dialogConfig1.buttons"
            width="700px"
            :showCancel="false"
            @close="closeDialog1">

            <el-form
            :rules="rules"
            ref="formDataRef"
            label-width="80px"
            @submit.pervent
            >
              <el-form-item label="tag">
                <el-select
                clear-icon="close"
                clearable
                v-model="addedTags.tag_ids"
                filterable
                multiple
                collapse-tags
                collapse-tags-tooltip
                placeholder="请选择tag"
                :style="{ width: '100%' }"
                @change="handleSegment3Change"
                >
                  <el-option
                    v-for="(item, index) in tags"
                    :key="item.tag_id"
                    :label="item.name"
                    :value="item.tag_id"
                    >
                    <span>
                      <el-checkbox v-model="checkTags[index]" />
                      <span class="select-text">{{ item.name }}</span>
                    </span>
                  </el-option>
                </el-select>
              </el-form-item>
            </el-form>
            </Dialog>
           
          </el-form-item>
        </div>
        
    <div class="post-separator"></div>
    <el-form-item v-if="postCache.username==userMessage.username">
      <el-button
      type="primary"
      size="large"
      @click="showDialog">
        添加商品
      </el-button>
      <Dialog
        :show="dialogConfig.show"
        :title="dialogConfig.title"
        :buttons="dialogConfig.buttons"
        width="700px"
        :showCancel="false"
        @close="dialogConfig.show = false">        
        <el-form
            :model="comFormData"
            :rules="rules"
            ref="formDataRef"
            label-width="80px"
            @submit.pervent
          >
          <el-form-item>
                <h2>创建商品</h2>
                <el-form-item label="title">
                   <div class="modal-content">
                        <el-input
                        :rows="3"
                        size="large"
                        placeholder="请输入商品名称"
                        v-model.trim="comFormData.name"
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
                        
                        placeholder="请输入商品详情"
                        v-model.trim="comFormData.dc"
                        ></el-input>
                   </div>
                </el-form-item>
                <el-form-item label="price">
                    <div class="modal-content">
                        <el-input
                        style="width: 250px"
                        height="250px"
                        :rows="20"
                        placeholder="请输入商品价格"
                        v-model.trim="comFormData.price"
                        ></el-input>
                   </div>
                </el-form-item>
            </el-form-item>
        </el-form>
    </Dialog>
    </el-form-item>
    
  

    <p>帖子包含商品：</p>
    <div>
      <PostGoodTable
        :commodities="commodities"
        :post_id="postCache.post_id"
        :post_user="postCache.username">
      </PostGoodTable>
    </div>

    </div>
                
             
</template>

<script setup>

import {ref, reactive, getCurrentInstance, nextTick, onMounted } from "vue";
import {useRouter, useRoute} from "vue-router";



import {createPost, getPost, getPostCommodities, createCommodity, 
  addCommodityPicture, getCommodityPictures, checkIfOrdered, 
  allTags, getTagDetail, getPostTags, deleteTagToPost, addTagToPost,
} from '../../api/postFunc';
import Dialog from '../../components/Dialog.vue';
import PostGoodTable from "@/components/PostGoodTable.vue";

const { proxy } = getCurrentInstance();
const router = useRouter();
const route = useRoute();

const userMessage = ref({
  "username" : proxy.VueCookies.get("userInfo").name,
})

const postCache = ref({
    "content" : "123",
    "title" : "title",
    "username" : "qwp",
    "data" : "2021/1/1",
    "post_id" : route.params.post_id,
    "dialog" : false,
    
});

//每个帖子的tags
const postTags = ref([]);

//所有tags?
const tags = ref([
  {
    "tag_id":1,
    "name" : "tag0_test",
  },
  {
    "tag_id":2,
    "name" : "name2",
  },
]);

//true->选择
const checkTags = ref({});

const handleSegment3Change = (val)=> {
  tags.value.forEach((item, index)=>{
    if (val && val.includes(item.tag_id)) {
        checkTags.value[index] = true;
    } else {
      checkTags.value[index] = false;
    }
  });
};



const getAllTags = async() => {
    var data = allTags();
    data.then((result)=>{
      tags.value = result.all_tags;
      //console.log(tags.value[0].tag_id);
      //console.log(tags.value[0].name);
    });
};

const judgeTagInPosts = (tag_id)=> {
  return postTags.value.some(post_tag => post_tag.tag_id === tag_id);
}



const deleteTag = async (tag_id)=> {
  
  proxy.Confirm(`你确定要删除该tag吗`, async() => {
    var params = {
    "tag_id" : tag_id,
    "post_id" : postCache.value.post_id,
    };
    
    var data = deleteTagToPost(params);
    data.then((result)=>{
      if (result.value == 0) {
        proxy.Message.success("删除tag成功");
        //initTag();
        router.go();
      } else {
        proxy.Message.error("删除tag失败");
      }
    });
  });
}

const addTag = async (tag_id)=> {
    var params = {
      "tag_id" : String(tag_id),
      "post_id" : postCache.value.post_id,
    };
    
    var data = addTagToPost(params);
    data.then((result)=>{
      console.log(result);
      if (result.value != 0) {
        proxy.Message.error("添加tag失败");
      }
    });
};

const addTags = async()=> {
  tags.value.forEach(async(item, index)=>{
    console.log(checkTags.value[index]);
    if (checkTags.value[index] && !judgeTagInPosts(item.tag_id)) {
      addTag(item.tag_id);  
    } 
  });
  /*console.log(addedTags.value.tag_ids.length);
  for (var tag in addedTags.value.tag_ids) {
    console.log(tags.value[0].tag_id);
    console.log(tags.value[tag].tag_id);
    addTag(tags.value[tag].tag_id);
  }*/
  //initTag();
  router.go();
};

const closeDialog1 = ()=> {
  Object.assign(addedTags.value ,ref({}));
  dialogConfig1.show = false;
}

const dialogConfig = reactive({
        show: false,
        title: "创建商品",
        buttons: [
        {
        type: "primary",
        text: "提交",
        click: () => {
            addCommodity(comFormData.value);
            console.log("submit!");
            comFormData.value = {};
          },
        },
        ],
});

const showDialog = ()=> {
  dialogConfig.show = true;
};

const addedTags = ref({});

const dialogConfig1 = reactive({
        show: false,
        title: "添加tags",
        buttons: [
        {
        type: "primary",
        text: "提交",
        click: () => {
            addTags();
            //console.log("submit!");

          },
        },
      ],
});

const showDialog1 = ()=> {
  dialogConfig1.show = true;
};

const comFormData = ref({});

const commodities = ref([
    {
        'commodity_id': "1",
        'name': "item.name",
        'dc': "item.description",
        'price': "item.price",
        'state': 0,
        'photos' :[{
          'photo_id': "photo_1",
          'path': "path_1",
          }
        ],
    },
    {
      'commodity_id': "2",
        'name': "testCom2",
        'dc': "dec2",
        'price': "120",
        'state': 0,
        'photos' :[{
          'photo_id': "photo_2",
          'path': "path_2",
          }
        ],
    },


]);


onMounted(() => {
    initData();
});

const initPost = async()=>{
  //console.log(postCache.value.post_id);

  //post
  var data1 = getPost(postCache.value.post_id);
  data1.then((result)=>{
    postCache.value.content = result.content;
    postCache.value.title = result.title;
    postCache.value.data = result.data;
    postCache.value.username = result.username;
  });
 
}

const initCom = async()=>{
    //commodities
    var result = await getPostCommodities(postCache.value.post_id);
    Object.assign(commodities.value ,result.commodities);
        //photos 遍历每个commodity
        for(const element of commodities.value) {
          //console.log(element.commodity_id);
          var result2 = await checkIfOrdered(element.commodity_id);
          element.state = result2.value;
          //console.log(result2.value);
          var result1 = await getCommodityPictures(element.commodity_id);
          element.photos = result1.pictures;
          //console.log(element.photos[0]);
        }
};

const initTag = async()=> {
    getAllTags();
    //获取所有该帖子的tags
    var result = await getPostTags(postCache.value.post_id);
      if (result.value == 0) {
        //proxy.Message.success("获取帖子tag成功");
        //console.log(result.tag_ids.length);

        result.tag_ids.forEach(async (tag_id)=> {
          //console.log(tag_id);
          if (tag_id != 0) {
            var detail = await getTagDetail(tag_id);
           
            //console.log(detail.name);
            postTags.value.push({
            "name" :  detail.name,
            "tag_id" : tag_id,
          });
        }
        });
      } else {
        proxy.Message.error("获取帖子tag失败");
      }
    
      //[int]
    
}

const initData = async()=> {
    initPost();
    initCom();
    //Tag
    initTag();

};

const addCommodity = (item)=> {
    var params = {
      "name" : item.name,
      "dc" : item.dc,
      "price" : item.price,
      "post_id" : postCache.value.post_id,
    };
    var data = createCommodity(params);
    
    data.then((result)=>{
      if (result.value == 0) {
        proxy.Message.success("创建商品成功");
        //initCom();
        router.go();
      } else {
        proxy.Message.console.error("创建商品失败");
      }
      // result.commodity_id;
    });
  
};


const addComPhoto = (item)=>{
    var data = addCommodityPicture(item);
    data.then((result)=>{
      if (result.value == 0) {
        proxy.Message.success("添加图片成功");
      } else {
        proxy.Message.error("添加图片失败");
      }
      //photo_id
    });
};


</script>

<style scoped>

.tag {
  display: inline-block;
  margin-right: 5px;
  padding: 5px;
  background-color: #f0f0f0;
}

.post-info {
  margin-bottom: 5px;
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

.card{
  color: "#F5F5F5";
  margin-top: 20px;
}

.v-card-title {
  font-size: 24px; 
  font-weight: bold;
}

.v-card-subtitle {
  font-size: 16px;
}

.v-divider {
  margin-top: 10px;
}

.show-img-slide {
  margin-top: 30px;
}

.edit-btn, .delete-btn, .comment-btn, .cart-btn, .cart-check-btn, .show-btn, .report-btn{
  position: fixed;
  display: inline-grid;
  z-index: 9999;
}

.comment-btn {
  right: 1.5em;
  bottom: 6.5em;
}

.cart-check-btn {
  right: 1.5em;
  bottom: 16.5em;

}
.edit-btn {
  right: 1.5em;
  bottom: 21.5em;
}

.delete-btn {
  right: 6.5em;
  bottom: 1.5em;
}

.cart-btn {
  right: 1.5em;
  bottom: 16.5em;
}

.show-btn {
  right: 1.5em;
  bottom: 1.5em;
}

.report-btn {
  right: 1.5em;
  bottom: 11.5em;
}

.comments {
  margin-top: 50px;
  margin-bottom: 50px;
}

.markdown {
  margin: 0 auto;
  border: none !important;
  background-color: white !important;
  min-height: 0px;
  border-left-width: 0px;
  z-index: 0;
}

    
</style>