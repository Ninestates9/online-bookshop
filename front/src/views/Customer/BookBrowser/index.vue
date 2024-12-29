<template>
  <div class="rightmain">
    <div class="righttop">
      <div class="mt-4">
        <el-input v-model="searchInput" style="max-width: 600px" placeholder="请输入搜索内容" class="input-with-select">
          <template #prepend>
            <el-select v-model="store.searchOP" placeholder="类型" style="width: 115px">
              <el-option label="书号" value=" Bno" />
              <el-option label="书名" value="Bname" />
              <el-option label="出版社" value="press" />
              <el-option label="关键字" value="key" />
              <el-option label="第一作者" value="author1" />
              <el-option label="第二作者" value="author2" />
              <el-option label="第三作者" value="author3" />
              <el-option label="第四作者" value="author4" />
            </el-select>
          </template>
          <template #append>
            <el-button :icon="Search" @click="getBookBrowser"/>
          </template>
        </el-input>
      </div>
    </div>
    <div class="bookbrowser">
      <el-card v-for="book in books" :key="book.Bno" class="book-card">
        <img :src="store.ip + '/cover/' + book.cover" alt="书本封面" class="book-cover" />
        <div class="book-info">
          <h3>{{ book.Bname }}</h3>
          <p>{{ book.authors.join(', ') }}</p>
          <p>¥{{ book.price }}</p>
        </div>
        <el-button size="small" @click="openPurchaseModal(book)">查看详情</el-button>
      </el-card>
      <el-dialog v-model="isModalOpen" title="书籍详情">
        <div>
          <img :src="store.ip + '/cover/' + selectedBook?.cover" alt="书本封面" class="detail-book-cover" />
          <p>书号: {{ selectedBook?.Bno }}</p>
          <p>丛书号: {{ selectedBook?.Bsubno }}</p>
          <h3>{{ selectedBook?.Bname }}</h3>
          <p>作者: {{ selectedBook?.authors.join(', ') }}</p>
          <p>关键字: {{ selectedBook?.keys.join(', ') }}</p>
          <p>出版社: {{ selectedBook?.press }}</p>
          <p>价格: ¥{{ selectedBook?.price }}</p>
          <p>库存: {{ selectedBook?.quantity }}</p>
          <p>目录: {{ selectedBook?.catalog }}</p>
          <p>位置: {{ selectedBook?.position }}</p>
          <el-input-number v-model="orderQuantity" :min="1" :max="selectedBook?.quantity" label="选择数量" />
        </div>
        <template #footer>
          <el-button @click="isModalOpen = false">取消</el-button>
          <el-button type="primary" @click="addToCart">确认购买</el-button>
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
import { Search } from '@element-plus/icons-vue'
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

const openPurchaseModal = (book) => {
  selectedBook.value = {
    Bno: book.Bno,
    Bsubno: book.Bsubno,
    Bname: book.Bname,
    authors: book.authors,
    press: book.press,
    price: book.price,
    quantity: book.quantity,
    cover: book.cover, // Include the cover image for detail view
    keys: book.keys,
    catalog: book.catalog,
    position: book.position,
  };
  orderQuantity.value = 1; // Reset quantity
  isModalOpen.value = true;
};

// 更新选中的搜索选项
const updateSearchOption = () => {
  store.searchOP = selectedOption.value; // 保存到 store
  // alert(store.searchOP);
};

// 书籍数据
const books = ref([

]);


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
  display: flex;
  /* 使用 flexbox 进行布局 */
  flex-wrap: wrap;
  /* 允许换行 */
  justify-content: flex-start;
  /* 左对齐 */
  background-color: rgba(233, 58, 5, 0.421);
  width: 100%;
  /* 确保容器宽度为 100% */
  padding: 10px;
  overflow-y: auto;
  /* 允许垂直滚动 */
}

.book-card {
  flex: 0 1 calc(33% - 20px);
  /* 每个卡片占据三分之一的宽度，减去边距 */
  display: flex;
  flex-direction: column;
  /* 垂直排列内容 */
  justify-content: space-between;
  /* 内容均匀分布 */
  height: 450px;
  /* 固定高度 */
  margin: 10px;
  /* 卡片之间的间距 */
  border-radius: 8px;
  /* 圆角 */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  /* 阴影效果 */
  box-sizing: border-box;
  /* 包含边距和填充在宽高内 */
}

.book-cover {
  width: 100%;
  /* 充满宽度 */
  height: 200px;
  /* 固定高度 */
  object-fit: cover;
  /* 保持比例并覆盖 */
}

.book-info {
  padding: 10px;
  /* 文本内边距 */
  flex-grow: 1;
  /* 允许文本区域占用剩余空间 */
  display: flex;
  flex-direction: row;
}



.detail-book-cover {
  width: 50%;
  height: auto;
  margin-bottom: 10px;
}
</style>