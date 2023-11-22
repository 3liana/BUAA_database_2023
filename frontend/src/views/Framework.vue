<template>
    <div class="framework">
        <div class="header">
            <div class="logo">
                
                <div class="name">北航十三公寓二手市场</div>
            </div>
            <div class="right-panel">
                <el-popover
                    :width="800"
                    trigger="click"
                    :v-model:visible="true"
                    :offset="20"
                    transition="none"
                    :hide-after="0"
                    :popper-style="{ padding: '0px' }"
                >
                <template #reference>
                    <span class="iconfont icon-transfer"></span>
                </template>
                <template #default>
                    暂时是上传区
                </template>
            </el-popover>

            <el-dropdown>
                <div class="user-info">
                    <div class="avatar">
                      <Avatar 
                      :name="userInfo.name" 
                      :avatar="userInfo.avatar"
                      :timestamp="timestamp"
                      :width="46"
                      v-if="userInfo && userInfo.name"
                      ></Avatar>
                    </div>
                    <span class="nick-name" v-if="userInfo">{{ userInfo.name }}</span>
                </div>
                <template #dropdown>
                    <el-dropdown-menu>
                        <el-dropdown-item @click="updateAvatar">修改头像</el-dropdown-item>
                        <el-dropdown-item>修改密码</el-dropdown-item>
                        <el-dropdown-item @click="logout">退出</el-dropdown-item>
                    </el-dropdown-menu>
                    
                </template>
            </el-dropdown>
            </div>
        </div>
        <div class="body">
            <div class="left-sider">
                <div class="menu-list">
                  <div @click="jump(item)" 
                  :class="['menu-item', item.menuCode==currentMenu.menuCode ? 'active':'']"
                     v-for="item in menus" >
                    <div :class="['iconfont', 'icon-' + item.icon]"></div>
                    <div class="text">
                      {{ item.name }}
                    </div>
                  </div>
                </div>
                <div class="menu-sub-list">
                  <div @click="jump(sub)" 
                  :class="['menu-item-sub', sub.menuCode==currentMenu.menuCode ? 'active':'']" 
                  v-for="sub in currentMenu.children">
                    <span :class="['iconfont', 'icon-'+sub.icon]" v-if="sub.icon"></span>
                    <span class="text">{{ sub.name }}</span>
                  </div>
                  <div class="tips" v-if="currentMenu&& currentMenu.tips">{{ currentMenu.tips }}</div>
                  <div class="space-info">
                    <div >空间使用</div>
                    <div class="percent"></div>
                  </div>
                </div>
            </div>
            <div class="body-content">
              <router-view v-slot="{ Component}">
                <component :is="Component">

                </component>
              </router-view>
            </div>
        </div>
        <!--修改头像-->
        <UpdateAvatar 
          ref="updateAvatarRef"
          @updateAvatar="reloadAvatar"
        ></UpdateAvatar>
    </div>
</template>

<script setup>
import {
  ref,
  reactive,
  getCurrentInstance,
  watch,
  nextTick,
  computed,
} from "vue";
import { useRouter, useRoute } from "vue-router";
import UpdateAvatar from "./UpdateAvatar.vue";
import Avatar from "../components/Avatar.vue";
import Dialog from "../components/Dialog.vue";


const { proxy } = getCurrentInstance();
const router = useRouter();
const route = useRoute();

const timestamp = ref(0);

//登录时已经将信息保存到cookie的
const userInfo = ref(proxy.VueCookies.get("userInfo"));

const menus = [
  {
    icon: "cloude",
    name: "首页",
    menuCode: "main",
    path: "/main/all",
    allShow: true,
    children: [
      {
        icon: "all",
        name: "主页",
        category: "all",
        path: "/main/all",
      },
      {
        icon: "music",
        name: "公告栏",
        category: "notice",
        path: "/main/notice",
      },
      {
        icon: "video",
        name: "交易栏",
        category: "deal",
        path: "/main/deal",
      },
      {
        icon: "more",
        name: "其他",
        category: "others",
        path: "/main/others",
      },
    ],
  },
  {
    path: "/myshare",
    icon: "share",
    name: "我发布的订单",
    menuCode: "share",
    allShow: true,
    children: [
      {
        name: "我发布的订单",
        path: "/myshare",
      },
    ],
  },
  {
    path: "/finished",
    icon: "del",
    name: "我购买的订单",
    menuCode: "finished",
    tips: "为你保存10天内完成的订单",
    allShow: true,
    children: [
      {
        name: "我购买的订单",
        path: "/finished/buyer",
      },
    ],
  },
  {
    path: "/settings/fileList",
    icon: "settings",
    name: "设置",
    menuCode: "settings",
    allShow: false,
    children: [
      {
        name: "用户文件",
        path: "/settings/fileList",
      },
      {
        name: "用户管理",
        path: "/settings/userList",
      },
      {
        path: "/settings/sysSetting",
        name: "系统设置",
      },
    ],
  },
];

const currentMenu = ref({});
const currentPath = ref();

const jump = (data)=> {
  if(!data.path || data.menuCode==currentMenu.menuCode) {
    //path为空或就是当前页面
    return;
  }
  console.log(proxy.VueCookies.get("userInfo").name);
  router.push(data.path);
};

const setMenu=(menuCode, path)=> {
  const menu = menus.find(item=> {
    return item.menuCode == menuCode;
  });
  currentMenu.value = menu;
  currentPath.value = path;
};

//监听路由
watch(
  () => route,
  (newVal, oldVal) => {
    if (newVal.meta.menuCode) {
      setMenu(newVal.meta.menuCode, newVal.path);
    }
  },
  { immediate: true, deep: true }
);

//修改头像
const updateAvatarRef = ref();
//调用上传头像函数
const updateAvatar = ()=> {
  updateAvatarRef.value.show(userInfo.value);
};
//回调函数，更新显示的头像
const reloadAvatar = ()=>{
  userInfo.value = proxy.VueCookies.get("userInfo");
  //timestamp.value = (new Data()).getTime();
};

//退出登录
const logout = () => {
  proxy.Confirm(`你确定要退出吗`, async() => {
    var value = logout();
    value.then((result) => {
        if (result.value != 0) {
          alert('登出错误');
          return;
        }
    });
    proxy.VueCookies.remove("userInfo");
    router.push("/login");
  });

};

</script>

<style lang="scss" scoped>
.header {
  box-shadow: 0 3px 10px 0 rgb(0 0 0 / 6%);
  height: 56px;
  padding-left: 24px;
  padding-right: 24px;
  position: relative;
  z-index: 200;
  display: flex;
  align-items: center;
  justify-content: space-between;

  .logo {
    display: flex;
    align-items: center;
    .icon-pan {
      font-size: 40px;
      color: rgb(88, 163, 212);
    }
    .name {
      font-weight: bold;
      margin-left: 5px;
      font-size: 25px;
      color: rgb(88, 163, 212);
    }
  }
  .right-panel {
    display: flex;
    align-items: center;
    .icon-transfer {
      cursor: pointer;
    }
    .user-info {
      margin-right: 10px;
      display: flex;
      align-items: center;
      cursor: pointer;
      .avatar {
        margin: 0px 5px 0px 15px;
      }
      .nick-name {
        color: rgb(88, 163, 212);
      }
    }
  }
}
.body {
  display: flex;
  .left-sider {
    border-right: 1px solid #f1f2f4;
    display: flex;
    .menu-list {
      height: calc(100vh - 56px);
      width: 80px;
      box-shadow: 0 3px 10px 0 rgb(0 0 0 / 6%);
      border-right: 1px solid #f1f2f4;
      .menu-item {
        text-align: center;
        font-size: 14px;
        font-weight: bold;
        padding: 20px 0px;
        cursor: pointer;
        &:hover {
          background: #f3f3f3;
        }
        .iconfont {
          font-weight: normal;
          font-size: 28px;
        }
      }
      .active {
        .iconfont {
          color: rgb(88, 163, 212);
        }
        .text {
          color: rgb(88, 163, 212);
        }
      }
    }
    .menu-sub-list {
      width: 200px;
      padding: 20px 10px 0px;
      position: relative;
      .menu-item-sub {
        text-align: center;
        line-height: 40px;
        border-radius: 5px;
        cursor: pointer;
        &:hover {
          background: #f3f3f3;
        }
        .iconfont {
          font-size: 14px;
          margin-right: 20px;
        }
        .text {
          font-size: 13px;
        }
      }
      .active {
        background: #eef9fe;
        .iconfont {
          color: rgb(88, 163, 212);
        }
        .text {
          color: rgb(88, 163, 212);
        }
      }

      .tips {
        margin-top: 10px;
        color: #888888;
        font-size: 13px;
      }

      .space-info {
        position: absolute;
        bottom: 10px;
        width: 100%;
        padding: 0px 5px;
        .percent {
          padding-right: 10px;
        }
        .space-use {
          margin-top: 5px;
          color: #7e7e7e;
          display: flex;
          justify-content: space-around;
          .use {
            flex: 1;
          }
          .iconfont {
            cursor: pointer;
            margin-right: 20px;
            color: rgb(88, 163, 212);
          }
        }
      }
    }
  }
  .body-content {
    flex: 1;
    width: 0;
    padding-left: 20px;
  }
}
</style>