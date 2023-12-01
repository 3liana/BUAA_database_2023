<template>
    <span class="avatar" :style="{ width: width + 'px', height: width + 'px' }">
      <img
        :src="'data:image/jpeg;base64,' + avatar"
        v-if="username"
      />
    </span>
  </template>


<script setup>
const props = defineProps({
    username: {
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