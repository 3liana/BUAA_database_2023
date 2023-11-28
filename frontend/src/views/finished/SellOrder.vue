<template>
    <div>
        <p>已完成的订单(卖出)</p>
        <div id="content" style="overflow:auto">
        <div class="common-list" >
          <div class="common-wrap" v-for="item in orders" :key="item.order_id">
            <div class="common-item">
              <div class="post-separator"></div>
              
             <router-link :to="`/main/post/${item.post_id}`"
              type="primary"
              size="large"
              class="post-title" 
             >{{ item.commodity_id }}</router-link>
              <div class="post-content">
                <p class="post-info">订单编号: {{ item.order_id }}</p>
                
                <p class="post-title">买家信息</p>
                <p class="post-info">买家: {{ item.buyer_id }}</p>
                <p class="post-info">电话号码: {{ item.phone }}</p>
                <p class="post-info">微信号: {{ item.wechat }}</p>

                <p class="post-info"> 卖家:{{ item.saler_id }}</p>

                <p class="post-info">交易于: {{ item.time }}</p>
                
              </div>
              </div>
              </div>
        </div>
        </div>

    </div>
</template>

<script setup>
    import {ref, reactive, getCurrentInstance, nextTick, onMounted } from "vue";
    import {useRouter, useRoute} from "vue-router";
    import {myOrdersAsSaler, getUserInfo, getOrder} from '../../api/postFunc';
    import Dialog from '../../components/Dialog.vue';
    

    const { proxy } = getCurrentInstance();

    const router = useRouter();
    const route = useRoute();

    const userMessage = ref({
        "username" : proxy.VueCookies.get("userInfo").name,
    });
    const orders = ref([]);
    const orderIds = ref([]);

    onMounted(()=>{
        initData();
    })

    const initData = async()=> {
        var data = myOrdersAsSaler(userMessage.value.username);
        data.then((result) => {
            if (result.value != 0) {
                proxy.Message.error("获取订单失败");
            } else {
                orderIds.value = result.order_ids;
                getContent();
            }
        });
    };

    const getContent = async()=> {
        orderIds.value.forEach(async (order_id)=> {
            var result = await getOrder(order_id);
            var userInfo = await getUserInfo(result.buyer_id);
            var result3 ;
            var params = {
                "order_id" : order_id,
                "saler_id" : result.saler_id,
                "buyer_id" : result.buyer_id,
                "phone" : userInfo.phone,
                "wechat" : userInfo.wechat,
                "commodity_id" : result.commodity_id,
                "post_id" : result3.commodity_id,
                "time" : result.time
            };
            
            orders.value.push(params);
        });
        
    };

</script>

<style lang="scss" scoped>
      .post-title {
    margin-bottom: 10px;
  font-size: 18px;
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
</style>