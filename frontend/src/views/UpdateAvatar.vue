<template>
    <div>
        <Dialog
        :show="dialogConfig.show"
        :title="dialogConfig.title"
        :buttons="dialogConfig.buttons"
        width="500px"
        :showCancel="true"
        @close="dialogConfig.show = false">
        
        <el-form
            :model="formData"
            ref="formDataRef"
            label-width="80px"
            @submit.prevent
        >
            <!--input输入-->
            <el-form-item label="用户名" prop="">
                {{ formData.name }}
            </el-form-item>
            <!--textarea输入-->
            <el-form-item label="头像" prop="">
                <AvatarUpload v-model="formData.avatar">
                </AvatarUpload>
            </el-form-item>
        </el-form>
    </Dialog>
    </div>
</template>
<script setup>
import AvatarUpload from '@/components/AvatarUpload.vue';
import Dialog from '@/components/Dialog.vue';
import { result } from 'lodash';
import {ref, reactive, getCurrentInstance} from "vue";
import { useRoute, useRouter } from 'vue-router';
import { setAvatar , getAvatar} from "../api/postFunc";

const { proxy } = getCurrentInstance();
const route = useRoute();
const router = useRouter();

const formData = ref({});
const formDataRef = ref();

const cookieUserInfo = proxy.VueCookies.get("userInfo");

const show = (data)=> {
    formData.value = Object.assign({}, data);
    formData.value.avatar = { name: data.name, avatar: data.avatar};
    dialogConfig.value.show = true;
};

defineExpose({show})

const dialogConfig = ref({
  show: false,
  title: "修改头像",
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

const emit = defineEmits(["updateAvatar"]);
const submitForm= async ()=> {
    if (!(formData.value.avatar instanceof File)) {
        dialogConfig.value.show = false;
        return;
    }
    //formData.value.name:->photo_name
    //p
    let params = {
        username: cookieUserInfo.name,
        photo: formData.value.avatar,
    };
    //console.log(params.username);
    //console.log(params.photo);
    var value;
    value = setAvatar(params);
    value.then((result)=>{
        console.log(result);
        //value? 
        //photo_id?
        if (!result)
            return;
    })
    
    dialogConfig.value.show = false;
    //更改photo
    cookieUserInfo.photo=params.photo;
    proxy.VueCookies.set("userInfo", cookieUserInfo, 0);
    emit("updateAvatar");
};

</script>

<style lang="scss" scoped>
</style>