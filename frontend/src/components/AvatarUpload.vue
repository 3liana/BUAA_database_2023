<template>
  <div class="avatar-upload">
    <div class="avatar-show">
      <template v-if="localFile">
        <img :src="localFile" />
      </template>
      <template v-else>
        <img :src="getMyAvatar()" />
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
  </div>
</template>

<script setup>
  import { ref, reactive, getCurrentInstance } from "vue";
import { useRouter, useRoute } from "vue-router";
import { getAvatar, getAvatorAdmin } from "../api/postFunc";
const { proxy } = getCurrentInstance();
const router = useRouter();
const route = useRoute();

const timestamp = ref("");

const props = defineProps({
  modelValue: {
    type: Object,
    default: null,
  },
});

const userMessage = ref({
  "usertype" : proxy.VueCookies.get("userInfo").usertype,
});

const localFile = ref(null);
const emit = defineEmits();
const uploadImage = async (file) => {
  file = file.file;
  let img = new FileReader();
  img.readAsDataURL(file);
  img.onload= ({ target }) => {
    localFile.value = target.result;
  };
  //modelValue = file;
  emit("update:modelValue", file);
};

const getMyAvatar = ()=>{
  if(userMessage.value.usertype == 0) {
    console.log(userMessage.value.usertype);
  var data = getAvatar(proxy.VueCookies.get("userInfo").name);
  data.then((result)=>{
    return result.base64;
  });
  } else {
    var data = getAvatorAdmin(proxy.VueCookies.get("userInfo").name);
    data.then((result)=>{
    return result.base64;
  });
  }
};

</script>

<style lang="scss">
.avatar-upload {
  display: flex;
  justify-content: center;
  align-items: end;
  .avatar-show {
    background: rgb(245, 245, 245);
    width: 150px;
    height: 150px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    position: relative;
    .iconfont {
      font-size: 50px;
      color: #ddd;
    }
    img {
      width: 100%;
      height: 100%;
    }
    .op {
      position: absolute;
      color: #0e8aef;
      top: 80px;
    }
  }
  .select-btn {
    margin-left: 10px;
    vertical-align: bottom;
  }
}
</style>