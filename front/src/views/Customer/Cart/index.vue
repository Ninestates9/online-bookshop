<template>
  <div class="rightmain">
      <div class="righttop">
          <h3 class="topinfo">购物车</h3>
      </div>
      <div class="cart">
          <div v-for="(book, index) in cartItems" :key="book.id" class="cart-item">
              <img :src="book.cover" alt="书本封面" class="book-cover" />
              <div class="book-details">
                <div class="basic-details">
                  <h4>{{ book.title }}</h4>
                  <p>作者: {{ book.author }}</p>
                  <p>单价: ¥{{ book.price }}</p>
                </div>
                  <div class="quantity-control">
                      <button @click="decreaseQuantity(index)">-</button>
                      <input type="number" v-model.number="book.quantity" min="1" />
                      <button  @click="increaseQuantity(index)">+</button>
                      <p>总价: ¥{{ (book.price * book.quantity).toFixed(2) }}</p>
                  </div>
                  <button class='deleteBtn' @click="removeItem(index)">删除</button>
              </div>
          </div>
          <div class="total">
              <h4>总计: ¥{{ totalPrice.toFixed(2) }}</h4>
          </div>
      </div>
  </div>
</template>
  
<script lang="ts" setup>
import { ref, computed } from 'vue';
import { mainStore } from '../../../store/index.ts';

const store = mainStore();

// 示例购物车书籍数据
const cartItems = ref([
    { id: 1, title: '书名1', author: '作者1', price: 50, quantity: 1, cover: '封面链接1' },
    { id: 2, title: '书名2', author: '作者2', price: 60, quantity: 2, cover: '封面链接2' },
    // 更多书籍
]);

const totalPrice = computed(() => {
    return cartItems.value.reduce((total, book) => total + book.price * book.quantity, 0);
});

// 方法：增加数量
const increaseQuantity = (index) => {
    cartItems.value[index].quantity++;
};

// 方法：减少数量
const decreaseQuantity = (index) => {
    if (cartItems.value[index].quantity > 1) {
        cartItems.value[index].quantity--;
    }
};

// 方法：删除书籍
const removeItem = (index) => {
    cartItems.value.splice(index, 1);
};

</script>
  
<style>
.cart {
    padding: 20px;
    font-size: 18px;
    text-align: left;
}

.cart-item {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
    border-bottom: 1px solid #ccc;
    padding-bottom: 15px;
}

.book-cover {
    width: 100px;
    height: auto;
    margin-right: 20px;
}

.book-details {
    display: flex;
    display: column;
}


.quantity-control {
    /* display: flex; */
    align-items: center;
}

.quantity-control input {
    width: 50px;
    text-align: center;
}

.quantity-control button {
  background-color: aliceblue;
  text-align: center;
  height: 40px;
  width: 20px;
}

.deleteBtn {
  background-color: aqua;
}
.total {
    margin-top: 20px;
    font-size: 20px;
    font-weight: bold;
}
</style>