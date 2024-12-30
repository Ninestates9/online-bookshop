<template>
  <div class="rightmain">
    <div class="righttop">
      <h3 class="topinfo">订单</h3>
    </div>
    <div class="history-order">
      <div v-if="orders.length > 0" class="order-list">

        <div v-for="(order, index) in orders" :key="index" class="order-item">
          <el-descriptions :border="true" column="2" class="order-header" size="large">
            <el-descriptions-item label="订单号">{{ order.Ono }}</el-descriptions-item>
            <el-descriptions-item label="总金额">{{ order.totalMoney }}</el-descriptions-item>
            <el-descriptions-item label="优惠金额">¥{{ order.discountMoney }}</el-descriptions-item>
            <el-descriptions-item label="订单状态"> ¥{{ order.state }}</el-descriptions-item>
            <el-descriptions-item label="下单时间"> {{ order.orderTime }}</el-descriptions-item>
            <el-descriptions-item label="送货地址"> {{ order.deliveryAddress }}</el-descriptions-item>
          </el-descriptions>
          <div class="order-details">
            <div>
              <div class="demo-collapse">
                <el-collapse v-model="activeNames" @change="handleChange">
                  <el-collapse-item title="书籍列表" name="1">
                    <el-table :data="order.books" border>
                      <el-table-column prop="Bname" label="书名" />
                      <el-table-column prop="authors" label="作者" :formatter="formatAuthors" />
                      <el-table-column prop="press" label="出版社" />
                      <el-table-column prop="price" label="单价" :formatter="formatPrice" />
                      <el-table-column prop="orderNumber" label="购买数量" />
                      <el-table-column prop="total" label="总价" :formatter="formatPrice" />
                    </el-table>
                  </el-collapse-item>
                </el-collapse>
              </div>

            </div>
            <div>

            </div>
          </div>
          <div class="order-actions">
            <!-- Ship Button -->
            <el-button type="success" @click="shipOrder(order.Ono)">发货</el-button>
            <!-- Arrive Button -->
            <el-button type="primary" @click="arriveOrder(order.Ono)">到货</el-button>
          </div>
        </div>
      </div>
      <div v-else>
        <p>暂无订单记录。</p>
      </div>
    </div>
  </div>
</template>


<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { mainStore } from '../../../store/index.ts';
import { ElMessage } from 'element-plus';
import axios from 'axios';

const store = mainStore();
const orders = ref([]); // 保存订单数据

// 获取订单数据
const getOrder = () => {
  axios({
    method: 'post',
    url: `${store.ip}/api/getOrders`,
    headers: { 'Content-Type': 'multipart/form-data' },
  })
    .then((response) => {
      let responseData = response.data;
      if (responseData.ret === 1) {
        ElMessage({
          message: responseData.msg,
          type: 'error',
          duration: 5 * 1000,
          grouping: true,
        });
      } else {
        orders.value = responseData.orders || []; // 更新订单数据
      }
    })
    .catch((error) => {
      console.error('获取订单失败:', error);
      ElMessage.error('获取订单失败，请稍后重试！');
    });
};

// 发货操作
const shipOrder = (Ono: string) => {
  let formData = new FormData();
  formData.append('Ono', Ono);
  // alert(formData.get('Ono'));
  axios({
    method: 'post',
    url: `${store.ip}/api/deliver`,
    data: formData,
  })
    .then((response) => {
      let responseData = response.data;
      if (responseData.ret === 1) {
        ElMessage({
          message: responseData.msg,
          type: 'error',
          duration: 5 * 1000,
          grouping: true,
        });
      } else {
        ElMessage({
          message: '订单已发货',
          type: 'success',
          duration: 5 * 1000,
          grouping: true,
        });
        getOrder(); // 刷新订单数据
      }
    })
    .catch((error) => {
      console.error('发货失败:', error);
      ElMessage.error('发货失败，请稍后重试！');
    });
};

// 到货操作
const arriveOrder = (Ono: string) => {
  let formData = new FormData();
  formData.append('Ono', Ono);
  axios({
    method: 'post',
    url: `${store.ip}/api/finish`,
    data: formData,
  })
    .then((response) => {
      let responseData = response.data;
      if (responseData.ret === 1) {
        ElMessage({
          message: responseData.msg,
          type: 'error',
          duration: 5 * 1000,
          grouping: true,
        });
      } else {
        ElMessage({
          message: '订单已到货',
          type: 'success',
          duration: 5 * 1000,
          grouping: true,
        });
        getOrder(); // 刷新订单数据
      }
    })
    .catch((error) => {
      console.error('到货失败:', error);
      ElMessage.error('到货失败，请稍后重试！');
    });
};

// 组件加载时获取订单数据
onMounted(() => {
  getOrder();
});
</script>


<style scoped>
.rightmain {
  position: relative;
  display: grid;
  grid-template-rows: 15% 85%;
  height: 98.5vh;
  width: 100%;
  overflow: hidden;
}

.righttop {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.topinfo {
  font-size: 50px;
  color: #fff;
}

.history-order {
  padding: 20px;
  font-size: 18px;
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
  color: black;
  background-color: #f9f9f9;
}

.books-list {
  margin-left: 20px;
}

.book-item {
  margin-bottom: 10px;
}

hr {
  margin: 10px 0;
  border-top: 1px solid #ccc;
}

p strong {
  font-weight: bold;
}
</style>
