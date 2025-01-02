<template>
    <div class="CustomerMain">
      <VantaBirds />
      <el-container>
        <el-aside width="20%">
          <div class="lefttop">
            <el-avatar class="av" shape="square" :size="90" :src="misakaImg" alt="Misaka Mikoto" fit="cover" />
            <h2 class="username">{{ store.username }}</h2>
          </div>
          <el-menu default-active="2" class="el-menu-vertical-demo">
            <el-menu-item index="1" @click="navigateTo('Storage')">
              <el-icon><Box /></el-icon>
              <span id="Storage">库存</span>
            </el-menu-item>
            <el-menu-item index="2" @click="navigateTo('Order')">
              <el-icon><Tickets /></el-icon>
              <span id="Order">订单</span>
            </el-menu-item>
            <el-menu-item index="3" @click="navigateTo('Usermessage')">
              <el-icon><ChatLineRound /></el-icon>
              <span id="Usermessage">消息</span>
            </el-menu-item>
            <el-menu-item index="4" @click="navigateTo('UserInfo')">
              <el-icon><User /></el-icon>
              <span id="UserInfo">用户信息</span>
            </el-menu-item>
            <el-menu-item index="5" @click="navigateTo('MissingRecord')">
              <el-icon><Warning /></el-icon>
              <span id="MissingRecord">缺书记录</span>
            </el-menu-item>
            <el-menu-item index="6" @click="navigateTo('Purchase')">
              <el-icon><DocumentAdd /></el-icon>
              <span id="MissingRecord" >采购单</span>
            </el-menu-item>
            <el-menu-item index="7" @click="navigateTo('Provider')">
              <el-icon><Shop /></el-icon>
              <span id="MissingRecord">供应商</span>
            </el-menu-item>
            <el-menu-item index="8" @click="logout()">
              <el-icon><SwitchButton /></el-icon>
              <span id="logout" style="color: red;">注销</span>
            </el-menu-item>
          </el-menu>
          <el-footer style="margin-top: 15px;">&copy; 2025 Online-bookshop. All rights reserved.</el-footer>
        </el-aside>
  
        <el-main width="80%" height="100%" style="padding: 0;">
          <router-view></router-view>
        </el-main>        
      </el-container>
    </div>
  </template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import misakaImg from '../../assets/images/vex.jpg';
import { mainStore } from '../../store/index.ts';
import { useRouter } from 'vue-router';
import axios from 'axios';
import VantaBirds from '../VantaBirds.vue';
const store = mainStore();
const router = useRouter();

function navigateTo(componentName) {
    // 路由导航
    router.push({ name: componentName });
}
const logout = () => {
    router.push({path:'/SignIn'})
}

const getuserinfo = () => {
  let uno = new FormData();
  uno.append('Uno', store.userid)
  axios({
    method: 'post',
    url: `${store.ip}/api/getInfo`,
    data: uno,
    headers: { 'Content-Type': 'multipart/form-data' }
  }
  )
    .then(response => {
      let responseData1 = response.data;
      store.username = responseData1.info.Uname;
      store.userlevel = responseData1.info.level;
      store.address = responseData1.info.address;
      store.balance = responseData1.info.balance;
    })
}
onMounted(() => {
  getuserinfo();

});
</script>

<style scoped>
.CustomerMain {
    left: 0%;
    top:0%;
    position: absolute;
    width: 100vw;
    /* 修正为 100vw */
    height: 98.5vh;
    overflow: hidden;
    background-color: rgba(135, 206, 250, 0.254);
}

.lefttop {
  padding: 10%;
  position: relative;
  display: flex;
  align-items: center;
}

.rightmain {
    position: relative;
    display: flex;
    height: 98.5vh;
    width: 100%;
    overflow: hidden;
    display: grid;
    grid-template-rows: 15% 85%;
}

.el-menu-vertical-demo span {
  font-size: 20px;
}

.el-menu-vertical-demo {
  width: 100%;
  height: 70%;
  min-height: 400px;
  padding: 5%;
}

.username {
  margin-left: 10%;
}

:deep(.switchIcon){
  color: red;
}
:deep(.el-aside) {
  background-color: rgba(62, 178, 255, 0.229);
}

:deep(.el-menu) {
  background-color: rgba(232, 251, 255, 0.229);

}

</style>