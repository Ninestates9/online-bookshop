<template>
  <div class="rightmain">
    <vanta-birds />
    <div class="righttop">
      <h3 class="topinfo">历史订单</h3>
    </div>
    <div class="history">
      <!-- 使用 v-for 显示历史订单 -->
      <div v-for="(order, index) in orders" :key="index" class="order-item">
        <div class="history-order">
          <el-descriptions :border="true" column="2" class="order-header" size="large">
            <el-descriptions-item label="订单时间">{{ order.orderTime }}</el-descriptions-item>
            <el-descriptions-item label="订单状态">{{ order.state }}</el-descriptions-item>
            <el-descriptions-item label="总金额">¥{{ order.totalMoney }}</el-descriptions-item>
            <el-descriptions-item label="优惠金额"> ¥{{ order.discountMoney }}</el-descriptions-item>
            <el-descriptions-item label="收货地址"> {{ order.deliveryAddress }}</el-descriptions-item>
          </el-descriptions>
          <div class="order-details">
            <el-collapse class="board">
              <el-collapse-item title="书籍列表" name="1" class="booklist">
                <el-table :data="order.books" class="book-table">
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
      </div>
    </div>
  </div>
</template>


<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { mainStore } from '../../../store/index.ts';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import VantaBirds from '../../VantaBirds.vue';
const store = mainStore();

const activeNames = ref(['1'])

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
  background-color: rgba(255, 255, 255, 0);
}

.righttop {
  width: 100%;
  padding: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 5%;
}

.topinfo {
  font-size: 30px;
  color: #333;
}

.history {
  font-size: 18px;
  text-align: center;
  overflow-y: auto;
  margin-bottom: 5%;
}

.order-item {
  padding-top: 20px;
}

.history-order {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.order-details {
  width: 90%;
  background-color: #33333300;
}

.order-header {
  width: 90%;
}

::v-deep .el-collapse-item__header:focus, .el-collapse-item__header:focus-visible {
    outline: none;
}

::v-deep .el-collapse-item__header {
    margin-left: 0;
}

</style>
