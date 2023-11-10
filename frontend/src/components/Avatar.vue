<template>
    <span class="avatar" :style="{ width: width + 'px', height: width + 'px'}">
        <img 
        :src="
        avatar && avatar!= '' ? avatar : '/api/getAvatar/'+`${name}`+`?${timestamp}`
        "
        v-if="name"
    >
    </span>
</template>


<script setup>
import { getCurrentInstance } from 'vue';
const { proxy } = getCurrentInstance();

const props = defineProps({
    name: {
        type: String,
    },
    avatar: {
        type: String,
    },
    timestamp: {
        type: Number,
        default: 0,
    },
    width: {
        type: Number,
        default: 40,
    },

});

</script>


<style lang="scss" scoped>
.avatar{
    display: flex;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    overflow: hidden;
    img {
        width: 100%;
        object-fit: cover;
    }
}
</style>