<template>
  <div class="rightmain">
    <div class="righttop">
      <h3 class="topinfo">用户信息</h3>
    </div>
    <div class="userinfo">
      <div v-for="user in users" :key="user.id" class="user-info">
        <div>
          <strong>账号:</strong> {{ user.userid }}
        </div>
        <div>
          <strong>昵称:</strong> {{ user.username }}
        </div>
        <div>
          <strong>信用等级:</strong> {{ user.userlevel }}
          <button @click="modifyCreditLevel(user.id)">修改信用等级</button>
        </div>
        <div>
          <strong>地址:</strong> {{ user.address }}
        </div>
        <div>
          <strong>余额:</strong> ¥{{ user.balance }}
        </div>
        <div>
          <strong>消费数额:</strong> ¥{{ user.total }}
        </div>
        <hr /> <!-- 分隔不同用户的信息 -->
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { mainStore } from '../../../store/index.ts';
import axios from 'axios';
import { ElMessage } from 'element-plus';

const store = mainStore();
const users = ref([]); // 用于存储多个用户的信息

const getUserInfo = () => {
  axios({
    method: 'post',
    url: `${store.ip}/api/getUserInfo`,
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  .then(response => {
    let responseData = response.data;
    if (responseData.ret === 1) {
      ElMessage({ message: responseData.msg, type: 'error', duration: 5 * 1000, grouping: true });
    } else {
      users.value = responseData.userinfo; // 假设 responseData.userinfo 是用户信息数组
    }
  })
  .catch(error => {
    console.error('获取用户信息失败:', error);
    ElMessage({ message: '获取用户信息失败', type: 'error', duration: 5 * 1000, grouping: true });
  });
};

const modifyCreditLevel = (userId) => {
  // 这里调用已有的方法来修改指定用户的信用等级
  console.log('修改用户信用等级的逻辑，用户ID:', userId);
};

onMounted(() => {
  getUserInfo(); // 组件挂载时获取用户信息
});
</script>

<style>
.rightmain {
  position: relative;
  display: flex;
  height: 98.5vh;
  width: 100%;
  overflow: hidden;
  display: grid;
  grid-template-rows: 15% 85%;
}

.righttop {
  position: relative;
  overflow: hidden;
  align-items: center;
  background-color: rgba(91, 247, 1, 0.421);
  width: 100%;
  height: 100%;
}

.topinfo {
  position: relative;
  width: 100%;
  height: 100%;
  align-items: center;
  font-size: 50px;
}

.userinfo {
  padding: 20px;
  font-size: 18px;
  text-align: left; /* 确保文本左对齐 */
}

.user-info {
  margin-bottom: 20px; /* 添加用户信息之间的间距 */
}

button {
  margin-left: 10px;
}
</style>