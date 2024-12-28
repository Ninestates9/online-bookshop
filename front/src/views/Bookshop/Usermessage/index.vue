<template>
    <div class="rightmain">
        <div class="righttop">
            <h3 class="topinfo">用户消息</h3>
        </div>
        <div class="message">
          <div v-for="message in messages" :key="message.Uno" class="user-message">
        <div>
          <strong>账号:</strong> {{ message.Uno }}
        </div>
        <div>
          <strong>消息：</strong> {{ message.message }}
        </div>
        <hr />
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
  const messages = ref([
  {
    Uno: 'U12345',
    message: '嘻嘻',
  },
]);
  const getUserMessage = () => {
    axios({
    method: 'post',
    url: `${store.ip}/api/getMsg`,
    headers: { 'Content-Type': 'multipart/form-data' },
  })
    .then((response) => {
      const responseData = response.data;
      if (responseData.ret === 1) {
        ElMessage({
          message: responseData.msg,
          type: 'error',
          duration: 5 * 1000,
          grouping: true,
        });
      } else {
        messages.value = responseData.messageSet;
      }
    })
  }

  const deleteUserMessage = (Uno) => {
    let formData = new FormData();
    FormData.append('Uno', Uno );
    axios({
    method: 'post',
    url: `${store.ip}/api/getMsg`,
    data: formData,
    headers: { 'Content-Type': 'multipart/form-data' },
  })
    .then((response) => {
      const responseData = response.data;
      if (responseData.ret === 1) {
        ElMessage({
          message: responseData.msg,
          type: 'error',
          duration: 5 * 1000,
          grouping: true,
        });
      } else {
        getUserMessage();
      }
    })
  }

  onMounted(() => {
    getUserMessage(); // 组件挂载时获取用户信息
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
  
  .message {
    padding: 20px;
    font-size: 18px;
    text-align: left; /* 确保文本左对齐 */
    overflow-y: auto
  }
  
  .user-message {
    margin-bottom: 20px;
  }
  
  button {
    margin-left: 10px;
  }
  </style>