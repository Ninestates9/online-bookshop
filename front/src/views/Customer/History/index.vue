<template>
  <div class="rightmain">
    <div class="righttop">
      <h3 class="topinfo">历史订单</h3>
    </div>
    <div class="history">
      <!-- 使用 v-for 显示历史订单 -->
      <div v-for="(order, index) in orders" :key="index" class="order-item">
        <el-descriptions :border="true" column="2" class="order-header">
          <el-descriptions-item label="订单时间">{{ order.orderTime }}</el-descriptions-item>
          <el-descriptions-item label="订单状态">{{ order.state }}</el-descriptions-item>
          <el-descriptions-item label="总金额">¥{{ order.totalMoney }}</el-descriptions-item>
          <el-descriptions-item label="优惠金额"> ¥{{ order.discountMoney }}</el-descriptions-item>
          <el-descriptions-item label="收货地址"> {{ order.deliveryAddress }}</el-descriptions-item>
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


const orders = ref([ // 将 orders 声明为响应式引用
  {
    books: [
      {
        Bname: "书籍名称",
        authors: ["作者1", "作者2"],
        press: "出版社",
        price: 100,
        orderNumber: 1,
        total: 100
      }
    ],
    totalMoney: 100,
    discountMoney: 10,
    deliveryAddress: "地址",
    state: "已完成",
    orderTime: "2024-12-25"
  }
]);

const getHistory = () => {
  let formData = new FormData();
  formData.append('Uno', store.userid); // 用户ID
  axios({
    method: 'post',
    data: formData,
    url: `${store.ip}/api/getHistory`,
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  .then(response => {
    let responseData = response.data;
    if (responseData.ret === 1) {
      ElMessage({ message: responseData.msg, type: 'error', duration: 5 * 1000, grouping: true });
    } else {
      orders.value = responseData.orders || []; // 正确更新 orders
    }
  })
  .catch(error => {
    ElMessage.error('获取历史订单错误');
  });
}

onMounted(() => {
  getHistory();
});

</script>

<style scoped>
.rightmain {
  display: grid;
  grid-template-rows: 15% 85%;
  height: 98.5vh;
}

.righttop {
  background-color: rgba(91, 247, 1, 0.421);
  width: 100%;
  padding: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.topinfo {
  font-size: 30px;
  color: #333;
}

.history {
  padding: 20px;
  font-size: 18px;
  text-align: left;
  overflow-y: auto;
}

.order-item {
  border-bottom: 1px solid #ddd;
  padding: 15px 0;
}

.order-header {
  font-weight: bold;
  margin-bottom: 10px;
}

.order-details {
  margin-top: 10px;
}

.order-details div {
  margin-bottom: 10px;
}

.order-details ul {
  list-style-type: none;
  padding-left: 0;
}

.order-details li {
  margin-bottom: 10px;
}

.order-details strong {
  font-size: 18px;
}
</style>
