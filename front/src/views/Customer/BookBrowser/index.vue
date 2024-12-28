<template>
  <div class="rightmain">
    <div class="righttop">
      <div class="searchbox">
        <input type="text" class="search-input" placeholder="请输入搜索内容" v-model="searchInput" />
        <button class="searchbtn" @click="getBookBrowser">搜索</button>
      </div>
      <div class="search-options">
        <label v-for="option in searchOptions" :key="option.value">
          <input type="radio" name="searchOption" :value="option.value" v-model="selectedOption"
            @change="updateSearchOption" />
          {{ option.label }}
        </label>
      </div>
    </div>
    <div class="bookbrowser">
      <el-row :gutter="20">
  <el-col v-for="book in books" :key="book.Bno" :span="24"> <!-- 设置 span 为 24 -->
    <el-card class="book-card">
      <img :src="store.ip+'/cover/' +book.cover" alt="书本封面" class="book-cover" />
      <div class="book-info">
        <p>书号: {{ book.Bno }}</p>
        <p>丛书号: {{ book.Bsubno }}</p>
        <h3>{{ book.Bname }}</h3>
        <p>作者: {{ book.authors }}</p>
        <p>关键字: {{ book.keys }}</p>
        <p>出版社: {{ book.press }}</p>
        <p>价格: ¥{{ book.price }}</p>
        <p>库存: {{ book.quantity }}</p>
        <p>目录: {{ book.catalog }}</p>
        <p>位置: {{ book.position }}</p>
        <el-button size="small" @click="openPurchaseModal(book)">购买</el-button>
      </div>
    </el-card>
  </el-col>
</el-row>


      <el-dialog v-model="isModalOpen" title="购买书籍">
        <div>
          <p>书名: {{ selectedBook?.Bname }}</p>
          <p>作者: {{ selectedBook?.authors.join(', ') }}</p>
          <p>出版社: {{ selectedBook?.press }}</p>
          <p>价格: ¥{{ selectedBook?.price }}</p>
          <el-input-number v-model="orderQuantity" :min="1" :max="selectedBook?.quantity" label="选择数量" />
        </div>
        <template #footer>
          <el-button @click="isModalOpen = false">取消</el-button>
          <el-button type="primary" @click="addToCart">确认</el-button>
        </template>
      </el-dialog>

    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { mainStore } from '../../../store/index.ts';
import { ElCard, ElRow, ElCol, ElMessage } from 'element-plus';
import axios from 'axios';
// 初始化 Pinia store
const store = mainStore();
const searchInput = ref(''); // 搜索输入框绑定的值
const isModalOpen = ref(false);
const selectedBook = ref(null);
const orderQuantity = ref(1);
const searchOptions = [
  { value: 'Bno', label: '书号' },
  { value: 'Bname', label: '书名' },
  { value: 'press', label: '出版社' },
  { value: 'key', label: '关键字' },
  { value: 'author1', label: '第一作者' },
  { value: 'author2', label: '第二作者' },
  { value: 'author3', label: '第三作者' },
  { value: 'author4', label: '第四作者' }
];

const selectedOption = ref('Bno'); // 默认选中的值

// 更新选中的搜索选项
const updateSearchOption = () => {
  store.searchOP = selectedOption.value; // 保存到 store
  // alert(store.searchOP);
};

// 书籍数据
const books = ref([
  { },
  // 更多书籍
]);

const openPurchaseModal = (book) => {
  selectedBook.value = {
    Bno: book.Bno,               // 确保包含书号
    Bsubno: book.Bsubno,         // 确保包含书号子编号
    Bname: book.Bname,
    authors: book.authors,
    press: book.press,
    price: book.price,
    quantity: book.quantity,
  };
  orderQuantity.value = 1; // 重置数量
  isModalOpen.value = true;
};


const addToCart = () => {
  if (!selectedBook.value) return;

  const cartItem = {
    Bno: selectedBook.value.Bno,   // 书号
    Bsubno: selectedBook.value.Bsubno, // 书号子编号
    Bname: selectedBook.value.Bname, // 书名
    authors: selectedBook.value.authors, // 作者
    press: selectedBook.value.press, // 出版社
    price: selectedBook.value.price, // 单价
    orderNumber: orderQuantity.value, // 购买数量
    total: selectedBook.value.price * orderQuantity.value, // 总价（你自己计算）
  };
  console.log(selectedBook.value.Bno); 
  store.cartItems.push(cartItem); // 添加到购物车
  ElMessage.success('已成功添加到购物车！');
  isModalOpen.value = false; // 关闭弹窗
};


const getBookBrowser = () => {
  // alert(store.searchOP);
  let formData = new FormData();
  formData.append('type', store.searchOP);
  formData.append('content', searchInput.value);
  axios({
    method: 'post',
    data: formData,
    url: `${store.ip}/api/searchBooks`,
    headers: { 'Content-Type': 'multipart/form-data' }
  })
    .then(response => {
      let responseData = response.data;
      console.log(responseData);
      if (responseData.ret === 1) {
        ElMessage({ message: responseData.msg, type: 'error', duration: 5 * 1000, grouping: true });
      } else {
        books.value = responseData.books;
      }
    }).catch(error => {
  console.error('Error fetching books:', error);
  ElMessage.error('请求失败，请稍后重试');
});
}
</script>

<style>
.rightmain {
  position: relative;
  display: grid;
  height: 98.5vh;
  width: 100%;
  grid-template-rows: 15% 85%;
}

.righttop {
  position: relative;
  overflow: hidden;
  background-color: rgba(91, 247, 1, 0.421);
  width: 100%;
  height: 100%;
}


.searchbox {
  position: relative;
  display: flex;
  align-items: center;
  background-color: rgba(91, 247, 1, 0.421);
  width: 100%;
  height: 50%;
  padding: 10px;
  overflow: hidden;
}

.search-input {
  width: 80%;
  padding: 10px;
  margin-left: 3%;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.searchbtn {
  background-color: rgba(163, 43, 218, 0.5);
  color: white;
  border: 1.5px solid rgba(176, 185, 15, 0.5);
  max-height: 100%;
  margin-right: 5px;
}

.search-options {
  display: flex;
  flex-wrap: wrap;
  /* 允许换行 */
  margin-top: 10px;
  /* 添加顶部边距 */
}

.search-options label {
  margin-right: 10px;
  /* 添加右侧间距 */
  color: #333;
  /* 可根据需要调整颜色 */
}

.bookbrowser {
  position: relative;
  display: flex;
  flex-wrap: wrap;  /* 允许内容换行 */
  justify-content: flex-start;  /* 元素靠左排列 */
  align-items: flex-start; /* 元素顶部对齐 */
  background-color: rgba(233, 58, 5, 0.421);
  width: 100%; /* 确保容器宽度为100% */
  height: 100%;
  padding: 10px;
  overflow-y: auto;
}


.book-card {
  max-width: 30%;
  width: 30%;  /* Ensures that each card can stretch to its container's width */
}


.book-cover {
  width: 100%;
  height: auto;
}
</style>