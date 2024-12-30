<template>
  <div class="rightmain">
    <div class="righttop">
      <h3 class="topinfo">缺书记录</h3>
    </div>
    <div class="missingRecord">
      <!-- Loop through shortageSet and display the details -->
      <div v-if="shortageSet.length > 0" class="order-list">
        <div v-for="(order, index) in shortageSet" :key="index" class="order-item">
          <el-checkbox v-model="selectedOrders" :label="order.Sno" size="large">
            <el-descriptions :border="true" column="3" style="width: 100%;">
              <el-descriptions-item label="订单号" label-width="100px">{{ order.Sno }}</el-descriptions-item>
              <el-descriptions-item label="书号" label-width="100px">{{ order.Bno }}</el-descriptions-item>
              <el-descriptions-item label="丛书号" label-width="100px">{{ order.Bsubno }}</el-descriptions-item>
              <el-descriptions-item label="书名" label-width="100px">{{ order.Bname }}</el-descriptions-item>
              <el-descriptions-item label="用户编号" label-width="100px">{{ order.Uno }}</el-descriptions-item>
              <el-descriptions-item label="缺货数量" label-width="100px">{{ order.insufficientNumber
                }}</el-descriptions-item>
              <el-descriptions-item label="缺货时间" label-width="100px">{{ order.time }}</el-descriptions-item>
            </el-descriptions>
          </el-checkbox>
        </div>
      </div>
      <div v-else>
        <p>暂无缺货记录。</p>
      </div>
      <div class="reg-sub-btn">
        <!-- Button to trigger modal -->
        <button @click="openModal" class="register-button">登记缺货订单</button>

        <!-- Button to submit selected orders -->
        <button @click="submitPurchaseOrder" class="submit-button">生成采购单</button>
      </div>
      <!-- Modal for registering shortage order -->
      <el-dialog :model-value="isModalVisible" title="登记缺货订单" style="width: 50%;" center>
        <el-form :model="newOrder" ref="orderForm" label-width="100px">
          <el-form-item label="书号">
            <el-input v-model="newOrder.Bno" placeholder="请输入书号" required></el-input>
          </el-form-item>
          <el-form-item label="丛书号">
            <el-input v-model="newOrder.Bsubno" type="number" placeholder="请输入丛书号" required></el-input>
          </el-form-item>
          <el-form-item label="缺货数量">
            <el-input v-model="newOrder.insufficientNumber" type="number" placeholder="请输入缺货数量" required></el-input>
          </el-form-item>
        </el-form>

        <span slot="footer" class="dialog-footer">
          <el-button @click="closeModal">取消</el-button>
          <el-button type="primary" @click="submitOrder">提交</el-button>
        </span>
      </el-dialog>
    </div>
  </div>
</template>



<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { mainStore } from '../../../store/index.ts';
import axios from 'axios';
import { ElMessage, ElDialog, ElButton, ElForm, ElFormItem, ElInput, ElCheckbox } from 'element-plus';

const store = mainStore();
const shortageSet = ref<any[]>([]);  // To store shortage orders
const selectedOrders = ref<number[]>([]);  // To store selected order numbers
const isModalVisible = ref(false); // To control modal visibility
const newOrder = ref({
  Bno: '',
  Bsubno: 0,
  insufficientNumber: 0,
}); // To store the new order data

// Function to get shortage orders from the API
const getShortageOrders = () => {
  axios({
    method: 'post',
    url: `${store.ip}/api/getShortage`,
    headers: { 'Content-Type': 'application/json' },
  })
    .then((response) => {
      let responseData = response.data;
      if (responseData.ret === 1) {
        ElMessage({
          message: responseData.msg,
          type: 'error',
          duration: 5 * 1000,
        });
      } else {
        shortageSet.value = responseData.shortageSet || [];  // Update the shortageSet
      }
    })
    .catch((error) => {
      console.error('获取缺货订单失败:', error);
      ElMessage.error('获取缺货订单失败，请稍后重试！');
    });
};

// Function to open the modal
const openModal = () => {
  isModalVisible.value = true;
};

// Function to close the modal
const closeModal = () => {
  isModalVisible.value = false;
  newOrder.value = { Bno: '', Bsubno: 0, Uno: '', insufficientNumber: 0 }; // Reset form
};

// Function to submit the order
const submitOrder = () => {
  // Validate required fields
  if (!newOrder.value.Bno || !newOrder.value.Bsubno || !newOrder.value.insufficientNumber) {
    ElMessage.error('请填写所有字段');
    return;
  }

  const formData = new FormData();
  formData.append('Bno', newOrder.value.Bno);
  formData.append('Bsubno', newOrder.value.Bsubno.toString());
  formData.append('Uno', store.userid);
  formData.append('insufficientNumber', newOrder.value.insufficientNumber.toString());

  // Sending the data via multipart/form-data
  axios({
    method: 'post',
    url: `${store.ip}/api/registerShortage`, // Make sure this is the correct endpoint for registration
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
    .then((response) => {
      if (response.data.ret === 0) {
        ElMessage.success('缺货订单登记成功');
        closeModal();  // Close modal after successful submission
        getShortageOrders();  // Reload shortage orders
      } else {
        ElMessage.error(response.data.msg);
      }
    })
    .catch((error) => {
      console.error('提交缺货订单失败:', error);
      ElMessage.error('提交缺货订单失败，请稍后重试！');
    });
};

// Function to submit selected shortage orders for purchase
const submitPurchaseOrder = () => {
  if (selectedOrders.value.length === 0) {
    ElMessage.error('请先选择缺货订单');
    return;
  }

  const formData = new FormData();
  formData.append('shortageSet', JSON.stringify(selectedOrders.value));

  // Sending the selected orders as a purchase order to the backend
  axios({
    method: 'post',
    url: `${store.ip}/api/purchase`, // Ensure this endpoint is correct
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
    .then((response) => {
      if (response.data.ret === 0) {
        ElMessage.success('采购单生成成功');
      } else {
        ElMessage.error(response.data.msg);
      }
    })
    .catch((error) => {
      console.error('生成采购单失败:', error);
      ElMessage.error('生成采购单失败，请稍后重试！');
    });
};

// Call the function on component mount to load shortage orders
onMounted(() => {
  getShortageOrders();
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
  text-align: center;
  margin-bottom: 20px;
}

.missingRecord {
  padding: 20px;
  font-size: 18px;
  text-align: left;
  overflow-y: auto;
}

.order-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.order-item {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #f9f9f9;
  display: flex;
  /* 使用 flexbox 布局 */
  flex-direction: column;
  /* 纵向排列内容 */
  min-height: 120px;
  /* 设置最小高度 */
  justify-content: center;
}


.el-checkbox__label p {
  margin: 5px 0;
  /* 设置段落之间的间距 */
  overflow: hidden;
  /* 隐藏溢出 */
  text-overflow: ellipsis;
  /* 使用省略号表示溢出文本 */
  white-space: nowrap;
  /* 不换行 */
}

hr {
  margin: 10px 0;
  border-top: 1px solid #ccc;
}

p strong {
  font-weight: bold;
}

.reg-sub-btn {
  display: flex;
  flex-grow: 1;
  justify-content: flex-end;
}

.register-button {
  position: relative;
  margin-top: 20px;
  margin-right: 20px;
  padding: 10px 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.register-button:hover {
  background-color: #45a049;
}

.submit-button {
  position: relative;
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.submit-button:hover {
  background-color: #0056b3;
}

::v-deep .el-checkbox {
  width: 100%;
  display: flex;
}

::v-deep .el-checkbox__label {
  width: 80%;
  flex-grow: 1;
}

.dialog-footer {
  display: flex;
  justify-content:space-around;
}

</style>
