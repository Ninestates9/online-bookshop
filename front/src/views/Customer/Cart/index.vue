<template>
  <div class="rightmain-cart">
    <VantaBirds />
    <div class="top">
      <h3 class="topinfo">购物车</h3>
    </div>
    <el-scrollbar class="cart">
      <div v-for="(book, index) in store.cartItems" :key="book.Bno + book.Bsubno" class="cart-item">
        <div class="book-details">
          <div>
            <p style="font-weight: bold;">{{ book.Bname }}</p>
          </div>
          <div class="detail-1">           
            <p>作者: {{ book.authors.join(', ') }}</p>
            <p style="padding-left: 30px;"> 出版社: {{ book.press }}</p>
          </div>
          <div class="detail-2">
            <p>书号: {{ book.Bno }}</p>
            <p style="padding-left: 30px;">丛书号: {{ book.Bsubno }}</p>
          </div>
        </div>
        <div class="book-control">
          <span>单价: ¥{{ book.price }}</span>
          <el-input-number v-model.number="book.orderNumber" :min="1" size="large"/>
          <span>总价: ¥{{ book.price * book.orderNumber }}</span>         
          <button class='deleteBtn' @click="removeItem(index)">删除</button>
        </div>
      </div>
    </el-scrollbar>
    <div class="bottom">
      <p>总价: ¥{{ totalPrice }}</p>
      <p>折扣后总价: ¥{{ getDiscount(totalPrice) }}</p>
      <button @click="submitCart" class="purchase">购买</button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue';
import { mainStore } from '../../../store/index.ts';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import VantaBirds from '../../VantaBirds.vue';
const store = mainStore();
const totalPrice = computed(() => {
  return Array.isArray(store.cartItems)
    ? store.cartItems.reduce((total, book) => total + (book.price * book.orderNumber), 0)
    : 0;
});

// 增加数量
const increaseQuantity = (index) => {
  store.cartItems[index].orderNumber++;
};

// 减少数量
const decreaseQuantity = (index) => {
  if (store.cartItems[index].orderNumber > 1) {
    store.cartItems[index].orderNumber--;
  }
};

// 删除书籍
const removeItem = (index) => {
  store.cartItems.splice(index, 1);
};

const getDiscount = (totalPrice) => {
  let discount;

  switch (store.userlevel) {
    case 1:
      discount = 0;
      store.overdraft = 0; // 0% 折扣
      break;
    case 2:
      discount = 0.05;
      store.overdraft = 0; // 5% 折扣
      break;
    case 3:
      discount = 0.1;
      store.overdraft = 100; // 10% 折扣
      break;
    case 4:
      discount = 0.15;
      store.overdraft = 500; // 15% 折扣
      break;
    case 5:
      discount = 0.2;
      store.overdraft = 99999999999; // 20% 折扣
      break;
    default:
      discount = 0;
      store.overdraft = 0; // 默认折扣
      break;
  }

  const discountPrice = totalPrice * (1 - discount);
  // alert(discountPrice);
  return discountPrice; // 返回折扣后的金额
};

const submitCart = () => {
  // alert(totalPrice.value);
  const discountPrice = getDiscount(totalPrice.value); // 获取折扣后的金额
  // alert(discountPrice);
  // 确保 discountPrice 是数字
  if (store.overdraft + store.balance >= discountPrice) {
    const cartData = store.cartItems.map(item => [
      item.Bno,          // 书号
      item.Bsubno,       // 丛书号
      item.orderNumber   // 数量
    ]);

    // 构建提交的数据
    let formData = new FormData();
    formData.append('Uno', store.userid); // 用户ID
    formData.append('books', JSON.stringify(cartData)); // 书籍数据

    // 提交购物车数据给后端
    axios({
      method: 'post',
      url: `${store.ip}/api/submitShoppingCart`,
      data: formData,
      headers: { 'Content-Type': 'multipart/form-data' }
    })
      .then(response => {
        let responseData = response.data;
        if (responseData.ret === 1) {
          ElMessage({ message: responseData.msg, type: 'error', duration: 5 * 1000, grouping: true });
        } else {
          // 购物车数据提交成功，接着提交订单
          let Uno = new FormData();
          Uno.append('Uno', store.userid);

          // 提交订单数据
          axios({
            method: 'post',
            url: `${store.ip}/api/submitOrder`, // 修正 URL
            data: Uno,
            headers: { 'Content-Type': 'multipart/form-data' }
          })
            .then(response => {
              let responseData = response.data;
              if (responseData.ret === 1) {
                ElMessage({ message: responseData.msg, type: 'error', duration: 5 * 1000, grouping: true });
              } else {
                // 如果订单提交成功，做后续操作
                ElMessage({ message: '订单提交成功', type: 'success' });
                store.cartItems = ref([]);
              }
            })
            .catch(error => {
              ElMessage.error('提交订单时出错');
            });
        }
      })
      .catch(error => {
        ElMessage.error('提交购物车时出错');
      });
  } else {
    ElMessage({ message: '账户余额不足', type: 'error' });
  }

};

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



</script>

<style>

.rightmain-cart {
  position: relative;
  display: flex;
  height: 98.5vh;
  width: 100%;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}

.rightmain-cart .cart {
  width: 100%;
  flex-grow: 1;
}

.rightmain-cart .top {
  margin-top: 5%;
}

.rightmain-cart .bottom{
  width: 60%;
  margin-bottom: 5%;
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.cart-item {
  display: flex;
  justify-content: flex-end;
  /* 使内容在行内均匀分布 */
  align-items: center;
  margin-bottom: 15px;
  border-bottom: 1px solid #ccc;
  padding-bottom: 15px;
}

.book-details {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  /* 垂直排列 */
  margin-left: 5%;
  align-items: flex-start;
}

.detail-1 {
  display: flex;
  flex-direction: row;
}

.detail-2 {
  display: flex;
  flex-direction: row;
}

.book-control {
  width: 60%;
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.purchase {
  background-color: aqua;
}

.total {
  margin-top: 20px;
  font-size: 20px;
  font-weight: bold;
}
</style>