<template>
    <div>
      <table>
        <thead>
          <tr>
            <th>Username</th>
            <th>电话号码</th>
            <th>WeChat</th>
            <th>是否被封禁</th>
            <th></th>
            <!-- Add more table headers as needed -->
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.username">
            <td>{{ user.username }}</td>
            <td>{{ user.phone }}</td>
            <td>{{ user.wechat }}</td>
            <td>{{ user.isBand }}</td>
            <td>
              <el-button
                v-if="userMessage.usertype == 1"
                @click="banUser(user.username)">
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
import { banAUser , allUsers} from '../../api/postFunc' 
const { proxy } = getCurrentInstance();
const router = useRouter();
const route = useRoute();
const users = ref([]);

onMounted(()=>{
  initData();
});

const userMessage = ref({
  "usertype" : proxy.VueCookies.get("userInfo").usertype,
})

const initData = async ()=>{
  var result = await allUsers();
  users.value = result.return_data;
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