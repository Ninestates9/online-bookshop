<template>
  <div class="rightmain">
    <div class="righttop">
      <h3 class="topinfo">历史订单</h3>
    </div>
    <div class="history">
      <!-- 使用 v-for 显示历史订单 -->
      <div v-for="(order, index) in orders" :key="index" class="order-item">
        <div class="order-header">
          <span>订单时间: {{ order.orderTime }}</span>
          <span>订单状态: {{ order.state }}</span>
        </div>
        <div class="order-details">
          <div>
            <strong>书籍列表:</strong>
            <ul>
              <li v-for="(book, bookIndex) in order.books" :key="bookIndex">
                <div>
                  <strong>{{ book.Bname }}</strong>
                  <p>作者: {{ book.authors.join(', ') }}</p>
                  <p>出版社: {{ book.press }}</p>
                  <p>单价: ¥{{ book.price }}</p>
                  <p>购买数量: {{ book.orderNumber }}</p>
                  <p>总价: ¥{{ book.total }}</p>
                </div>
              </li>
            </ul>
          </div>
          <div>
            <p>总金额: ¥{{ order.totalMoney }}</p>
            <p>优惠金额: ¥{{ order.discountMoney }}</p>
            <p>收货地址: {{ order.deliveryAddress }}</p>
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
