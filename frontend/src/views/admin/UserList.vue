<template>
    <div>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Username</th>
            <th>WeChat</th>
            <th></th>
            <!-- Add more table headers as needed -->
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.wechat }}</td>
            <td>
              <el-button @click="banUser(user.username)">
                封禁用户
              </el-button>
            </td>
            <!-- Add more table cells as needed -->
          </tr>
        </tbody>
      </table>
    </div>
  </template>

<script setup>
import {ref, reactive, getCurrentInstance, nextTick, onMounted } from "vue";
import {useRouter, useRoute} from "vue-router";
import { banAUser } from '../../api/postFunc' 
const { proxy } = getCurrentInstance();
const router = useRouter();
const route = useRoute();
const users = ref([]);

onMounted(()=>{
  initData();
});

const initData = ()=>{

};

const banUser = async (username)=>{
    var result = await banAUser(username);
    if (result.value == 0) {
        proxy.Message.success("封禁用户成功");
        router.go();
    } else {
        proxy.Message.error("封禁用户失败");
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