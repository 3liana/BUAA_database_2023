<template>
    <div>
        <p>已完成的订单(卖出)</p>
        <div id="content" style="overflow:auto">
        <div class="common-list" >
          
          <div class="seperate">
          <div class="common-wrap" v-for="item in orders" :key="item.order_id">
            <el-card class="box-card">
            <div class="common-item">
              
             <router-link :to="`/main/post/${item.commodity.post_id}`"
              type="primary"
              size="large"
              class="post-title" 
             >{{ item.commodity.name }}</router-link>
              <div class="post-content">
                <p class="post-info">商品详情: {{ item.commodity.dc }}</p>
                <p class="post-info">订单编号: {{ item.order_id }}</p>
              </div>

              <table>
                <tr><td>买家</td>
                  <td>{{ item.buyer_name }}</td>
                  
                </tr>
                <tr>
                  <td>电话号码</td>
                  <td>{{ item.phone }}</td>
                </tr>
                <tr>
                  <td>微信号</td>
                  <td>{{ item.wechat }}</td>
                </tr>
                <tr>
                  <td>卖家</td>
                  <td>{{ item.saler_name }}</td>
                </tr>
                <tr>
                  <td>交易时间</td>
                  <td>{{ item.time }}</td>
                </tr>
              </table>

              <div>
                <el-button @click="cancel(item.order_id)">
                  取消订单
                </el-button>
              </div>
              </div>
            </el-card>
              </div>
          </div>
        </div>
        </div>

    </div>
</template>

<script setup>
    import {ref, reactive, getCurrentInstance, nextTick, onMounted } from "vue";
    import {useRouter, useRoute} from "vue-router";
    import {myOrdersAsSaler, getUserInfo, getOrder, getCommodityDetail, cancelOrder} from '../../api/postFunc';
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
                //不存在
                //proxy.Message.error("获取订单失败");
            } else {
                orderIds.value = result.order_ids;
                getContent();
            }
        });
    };

    const getContent = async()=> {
        orderIds.value.forEach(async (order_id)=> {
            var result = await getOrder(order_id);
            var userInfo = await getUserInfo(result.buyer_name);
            var result3 = await getCommodityDetail(result.commodity_id);;
            var params = {
                "order_id" : order_id,
                "saler_name" : result.saler_name,
                "buyer_name" : result.buyer_name,
                "phone" : userInfo.phone,
                "wechat" : userInfo.wechat,
                "commodity" : {
                  "commodity_id" : result.commodity_id,
                  "name" : result3.name,
                  "dc" : result3.dc,
                  "price" : result3.price,
                  "post_id" : result3.post_id,
                },                
                "time" : result.time
            };
            
            orders.value.push(params);
        });
        
    };

    const cancel = (order_id)=>{
      var data = cancelOrder(order_id);
      data.then((result)=>{
        if (result.value == 0) {
          proxy.Message.success("取消订单成功");
          router.go();
        } else {
          proxy.Message.error("取消订单失败");
        }
      });
    };

</script>

<style lang="scss" scoped>
      .post-title {
    margin-bottom: 10px;
  font-size: 30px;
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

  // .post-separator {
  // height: 1px;
  // background-color: #ccc;
  // margin: 10px 0;
  // }

  .post-info {
  margin-bottom: 5px;
  font-size: 14px;
  font-weight: bold;
  }
  .seperate{
    display: flex;
    flex-direction:row;
    flex-wrap:wrap;
    justify-content:left;
  }

  .box-card {
  width: 500px;
  margin-right: 20px;
  margin-top: 20px;
}

table, td, th
{
    border:1px solid green;
}

td{
  text-align: center;
  padding: 10px;
}
.box-card {
  width: 500px;
}
.el-button{
  margin-top: 20px;
}
</style>