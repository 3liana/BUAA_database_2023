


<script setup>
import { getCurrentInstance, onMounted , ref} from 'vue';
import { getAvatar } from '../api/postFunc';

const { proxy } = getCurrentInstance();


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