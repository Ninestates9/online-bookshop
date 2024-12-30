<template>
  <div class="rightmain">
    <VantaBirds />
    <div class="righttop">
      <h3 class="topinfo">用户信息</h3>
    </div>
    <div class="userinfo">
      <div v-for="user in users" :key="user.Uno" class="user-info">

        <el-descriptions :border="true" column="2" size="large">
          <el-descriptions-item label="账号" label-width="120px">{{ user.Uno }}</el-descriptions-item>
          <el-descriptions-item label="昵称" label-width="120px">{{ user.Uname }}</el-descriptions-item>
        </el-descriptions>
        <el-descriptions :border="true" column="1" size="large">
          <el-descriptions-item label="地址" label-width="120px">{{ user.address }}</el-descriptions-item>
        </el-descriptions>
        <el-descriptions :border="true" column="3" size="large">
          <el-descriptions-item label="余额" label-width="120px">{{ user.balance }}</el-descriptions-item>
          <el-descriptions-item label="消费数额" label-width="120px">{{ user.total }}</el-descriptions-item>
          <el-descriptions-item label="信用等级" label-width="120px">
            <div class="m-userinfo-inline">
              <span>{{ user.level }}</span>
              <el-button @click="openDialog(user)">修改信用等级</el-button>
            </div>
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </div>

    <!-- 修改信用等级的对话框 -->
    <el-dialog v-model="isDialogVisible" title="修改信用等级" center>
      <div class="m-dialog-userInfo">
        <el-input v-model="newCreditLevel" type="number" placeholder="请输入新的信用等级" :min="0" :max="10" style="width: 60%; margin-bottom: 5%;margin-top: 5%;"></el-input>
        <span class="dialog-footer">
          <el-button size="large" @click="isDialogVisible = false">取消</el-button>
          <el-button size="large" type="primary" @click="submitCreditLevel">确定</el-button>
        </span>
      </div>
    </el-dialog>
  </div>
</template>


<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { mainStore } from '../../../store/index.ts';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import VantaBirds from '../../VantaBirds.vue';

const store = mainStore();
const users = ref([
  {
    Uno: 'U12345',
    Uname: '测试用户',
    level: 1,
    address: '测试地址',
    balance: 100.5,
    total: 250.75,
  },
]);

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
        users.value = responseData.userInfo; // 假设 responseData.userinfo 是用户信息数组
      }
    })
    .catch(error => {
      console.error('获取用户信息失败:', error);
      ElMessage({ message: '获取用户信息失败', type: 'error', duration: 5 * 1000, grouping: true });
    });
};

const isDialogVisible = ref(false); // 控制对话框显示
const newCreditLevel = ref(0); // 存储输入的新信用等级
const selectedUser = ref(null); // 当前选中的用户

// 打开对话框
const openDialog = (user) => {
  selectedUser.value = user; // 记录当前用户
  newCreditLevel.value = user.level; // 默认显示当前信用等级
  isDialogVisible.value = true; // 打开对话框
};

// 提交信用等级修改
const submitCreditLevel = () => {
  if (!selectedUser.value) return;

  // 构建表单数据
  let formData = new FormData();
  formData.append('Uno', selectedUser.value.Uno);
  formData.append('level', newCreditLevel.value);

  // 发送请求
  axios({
    method: 'post',
    url: `${store.ip}/api/updateUserInfo`,
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
        ElMessage({
          message: '信用等级修改成功',
          type: 'success',
          duration: 5 * 1000,
          grouping: true,
        });
        // 更新用户信息
        selectedUser.value.level = newCreditLevel.value;
      }
    })
    .catch((error) => {
      console.error('修改信用等级失败:', error);
      ElMessage({
        message: '修改信用等级失败',
        type: 'error',
        duration: 5 * 1000,
        grouping: true,
      });
    })
    .finally(() => {
      isDialogVisible.value = false; // 关闭对话框
    });
};


onMounted(() => {
  getUserInfo(); // 组件挂载时获取用户信息
});
</script>

<style scoped>
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
  text-align: left;
  /* 确保文本左对齐 */
  overflow-y: auto;
}


.user-info {
  margin-bottom: 20px;
  border-bottom: 1px solid #ccc;
  padding-bottom: 40px;
}

button {
  margin-left: 10px;
  background-color: aqua;
}

.m-userinfo-inline {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.m-dialog-userInfo {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-around;
}

.dialog-footer {
  width: 80%;
  display: flex;
  align-items: center;
  justify-content: space-around;
  margin-bottom: 5%;
}
</style>