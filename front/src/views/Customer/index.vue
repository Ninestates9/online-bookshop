<template>
  <div class="CustomerMain">
    <el-container>
      <el-aside width="20%">
        <div class="lefttop">
          <el-avatar class="av" shape="square" :size="100" :src="misakaImg" alt="Misaka Mikoto" fit="cover" />
          <h2 class="username">{{ store.username }}</h2>
        </div>
        <el-menu default-active="2" class="el-menu-vertical-demo">
          <el-menu-item index="1" @click="navigateTo('BookBrowser')">
            <el-icon><Search /></el-icon>
            <span id="BookBrowser">搜索书籍</span>
          </el-menu-item>
          <el-menu-item index="2" @click="navigateTo('CustomerInfo')">
            <el-icon><User /></el-icon>
            <span id="CustomerInfo">用户信息</span>
          </el-menu-item>
          <el-menu-item index="3" @click="navigateTo('Cart')">
            <el-icon><ShoppingTrolley /></el-icon>
            <span id="Cart" >购物车</span>
          </el-menu-item>
          <el-menu-item index="4" @click="navigateTo('History')">
            <el-icon><Tickets /></el-icon>
              <span id="History">历史订单</span>
          </el-menu-item>
          <el-menu-item index="5" @click="showDialog()">
            <el-icon><Message /></el-icon>
            <span id="Message" >留言</span>
          </el-menu-item>
          <el-menu-item index="6" @click="logout()">
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
import { ref, onMounted } from 'vue';
import misakaImg from '../../assets/images/Misaka Mikoto.jpg';
import { mainStore } from '../../store/index.ts';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';
const store = mainStore();
const router = useRouter();
const message = ref('');
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
const showDialog = () => {
  console.log('添加书目按钮被点击');
  dialogVisible.value = true;
};
const logout = () => {
  // 确保 cartItems 是有效且非空的
  if (store.cartItems.value && Array.isArray(store.cartItems.value)) {
    const cartData = store.cartItems.map(item => [
      item.Bno,          // 书号
      item.Bsubno,       // 丛书号
      item.orderNumber   // 数量
    ]);

    // 构建提交的数据
    let formData = new FormData();
    formData.append('Uno', store.userid); // 用户ID
    formData.append('books', JSON.stringify(cartData)); // 将二维数组转为JSON字符串传给后端

    // 提交购物车数据给后端
    axios({
      method: 'post',
      data: formData,
      url: `${store.ip}/api/submitShoppingCart`,
      headers: { 'Content-Type': 'multipart/form-data' }
    })
      .then(response => {
        let responseData = response.data;
        if (responseData.ret === 1) {
          ElMessage({ message: responseData.msg, type: 'error', duration: 5 * 1000, grouping: true });
        } else {
          router.push({ path: '/SignIn' })
        }
      })
      .catch(error => {
        ElMessage.error('提交购物车时出错');
      });
  } else {
    router.push({ path: '/SignIn' })
  }
};

const dialogVisible = ref(false);

const sendMessage = () => {
  let formData = new FormData();
  formData.append('Uno', store.userid);
  formData.append('message', message.value);
  axios({
    method: 'post',
    url: `${store.ip}/api/sendMsg`,
    data: formData,
    headers: { 'Content-Type': 'multipart/form-data' }
  }
  )
    .then(response => {
      let responseData = response.data;
      if (responseData.ret === 1) {
        ElMessage({ message: responseData.msg, type: 'error', duration: 5 * 1000, grouping: true });
      }
      else {
        getuserinfo();
      }
    });
  dialogVisible.value = false;
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
// 获取购物车数据
const getCartBook = () => {
  let formData = new FormData();
  formData.append('Uno', store.userid);
  axios({
    method: 'post',
    data: formData,
    url: `${store.ip}/api/getShoppingCart`,
    headers: { 'Content-Type': 'multipart/form-data' }
  })
    .then(response => {
      let responseData = response.data;
      if (responseData.ret === 1) {
        ElMessage({ message: responseData.msg, type: 'error', duration: 5 * 1000, grouping: true });
      } else {
        // 确保数据结构正确
        store.cartItems.value = responseData.books.map(book => ({
          ...book,
          authors: Array.isArray(book.authors) ? book.authors : [book.authors],
          orderNumber: book.orderNumber || 1,
          total: book.total || book.price * (book.orderNumber || 1)
        }));
      }
    });
};

onMounted(() => {
  if (!store.cartItems || store.cartItems.length === 0) {
    store.cartItems = []; // 确保是数组
  }
  getCartBook();
});

import {
  Document,
  Menu as IconMenu,
  Location,
  Setting,
} from '@element-plus/icons-vue'
</script>

<style>
.CustomerMain {
  left: 0%;
  top: 0%;
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.lefttop {
  padding: 10%;
  position: relative;
  display: flex;
  align-items: center;
}

.username {
  margin-left: 10%;
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
</style>