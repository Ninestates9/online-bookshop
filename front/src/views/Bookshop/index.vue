<template>
    <div class="CustomerMain">
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
          <el-footer>&copy; 2025 Online-bookshop. All rights reserved.</el-footer>
        </el-aside>
  
        <el-main width="80%" height="100%">
          <router-view></router-view>
        </el-main>        
      </el-container>
    </div>
  </template>

<script lang="ts" setup>
import { ref } from 'vue';
import misakaImg from '../../assets/images/vex.jpg';
import { mainStore } from '../../store/index.ts';
import { useRouter } from 'vue-router';
const store = mainStore();
const router = useRouter();

function navigateTo(componentName) {
    // 路由导航
    router.push({ name: componentName });

    // // 获取当前选中的按钮
    // let currentButton = document.getElementById(componentName);
    // const buttons = document.querySelectorAll('.nav-button'); // 假设按钮有类 'nav-button'

    // // 设置当前按钮的样式（例如背景颜色和文本颜色）
    // if (currentButton) {
    //     currentButton.style.backgroundColor = '#007bff'; // 设置选中的按钮背景色
    //     currentButton.style.color = '#ffffff'; // 设置选中按钮的文本颜色
    // }

    // // 重置其他按钮的样式
    // buttons.forEach(button => {
    //     if (button.id !== componentName) {
    //         button.style.backgroundColor = ''; // 重置为默认背景色
    //         button.style.color = ''; // 重置为默认文本颜色
    //     }
    // });
}
const logout = () => {
    router.push({path:'/SignIn'})
}
</script>

<style>
.CustomerMain {
    left: 0%;
    top:0%;
    position: absolute;
    width: 100vw;
    /* 修正为 100vw */
    height: 98.5vh;
    overflow: hidden;
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

</style>