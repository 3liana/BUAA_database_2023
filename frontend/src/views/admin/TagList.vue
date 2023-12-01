<template>
    <div>
        <el-form-item>
            <el-button
            v-if="userMessage.usertype==1"
            type="primary"
            size="large"
            @click="showDialog">
                创建tag
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
                <el-form-item label="content">
                   <div class="modal-content">
                        <el-input
                        :rows="3"
                        size="large"
                        placeholder="请输入tag名"
                        v-model.trim="formData.name"
                        ></el-input>
                   </div>
                </el-form-item>
                </el-form>
            </Dialog>


        </el-form-item>
    </div>
    <div>
      <table>
        <thead>
          <tr>
            <th>tag ID</th>
            <th>tag name</th>
            <th>tag 引用次数</th>
            <th></th>
            <!-- Add more table headers as needed -->
          </tr>
        </thead>
        <tbody>
          <tr v-for="tag in tags" :key="tag.tag_id">
            <td>{{ tag.tag_id }}</td>
            <td>{{ tag.name }}</td>
            <td>{{ tag.num }}</td>
            <td> <el-button
              v-if="userMessage.usertype==1"
               @click="deleteT(tag.tag_id)">
                删除tag
                </el-button></td>
            <!-- Add more table cells as needed -->
          </tr>
        </tbody>
      </table>
    </div>
  </template>

<script setup>
import {ref, reactive, getCurrentInstance, nextTick, onMounted } from "vue";
import {useRouter, useRoute} from "vue-router";
import Dialog from '../../components/Dialog.vue';
import { allTags, createTag, deleteTag } from "../../api/postFunc";
const { proxy } = getCurrentInstance();
const router = useRouter();
const route = useRoute();

const tags = ref([]);
const formData = ref({});
const userMessage = ref({
  "usertype" : proxy.VueCookies.get("userInfo").usertype,
});


onMounted(()=>{
    initData();
});



const initData = async ()=>{
    var result = await allTags();
    tags.value = result.all_tags;
};

const dialogConfig = reactive({
        show: false,
        title: "创建tag",
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

    const showDialog = ()=> {
        dialogConfig.show = true;
    };

const deleteT = async (tag_id) => {
    var result = await deleteTag(tag_id);
    if (result.value == 0) {
        proxy.Message.success("删除tag成功");
        router.go();
    } else {
        proxy.Message.error("删除tag失败");
    }
};

const submitPost = async ()=>{
    var result = await createTag(formData.value.name);
    if (result.value == 0) {
        proxy.Message.success("创建tag成功");
        router.go();
    } else {
        proxy.Message.error("创建tag失败");
    }

};

</script>

<style>
table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 8px;
  text-align: left;
  border-bottom: 1px solid #ddd;
} 

th {
  background-color: #f2f2f2;
}
</style>