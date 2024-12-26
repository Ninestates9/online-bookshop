<template>
  <div class="rightmain">
      <div class="righttop">
          <h3 class="topinfo">库存</h3>
      </div>
      <div class="storage">
          <div v-for="(book, index) in storageItems" :key="book.id" class="storage-item">
              <img :src="book.cover" alt="书本封面" class="book-cover" />
              <div class="book-details">
                  <div class="basic-details">
                      <p>书号: {{ book.id }}</p>
                      <h4>{{ book.title }}</h4>
                      <p>作者: {{ book.author }}</p>
                      <div class="price-control">
                          <label>价格: ¥</label>
                          <input type="number" v-model.number="book.price" min="0" />
                      </div>
                      <p>库存数量: {{ book.stock }}</p>
                  </div>
              </div>
          </div>
          <el-button type="primary" @click="showDialog">添加书目</el-button>
      </div>

      <el-dialog title="添加新书籍" :model-value="dialogVisible">
          <div>
              <el-upload
                  class="upload-demo"
                  action="#"
                  :show-file-list="false"
                  :on-change="handleImageChange"
                  :before-upload="beforeUpload"
                  accept="image/*">
                  <el-button size="small" type="primary">上传封面图</el-button>
              </el-upload>
              <el-input v-model="newBook.id" placeholder="书号"></el-input>
              <el-input v-model="newBook.title" placeholder="书名"></el-input>
              <el-input v-model="newBook.author" placeholder="作者"></el-input>
              <el-input v-model.number="newBook.price" type="number" placeholder="价格"></el-input>
              <el-input v-model.number="newBook.stock" type="number" placeholder="数量"></el-input>
          </div>
          <span slot="footer" class="dialog-footer">
              <el-button @click="dialogVisible = false">取 消</el-button>
              <el-button type="primary" @click="addBook">确 定</el-button>
          </span>
      </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { mainStore } from '../../../store/index.ts';
import axios from 'axios';
const store = mainStore();

// 示例存储书籍数据
const storageItems = ref([
    { id: 1, title: '书名1', author: '作者1', price: 50, stock: 100, cover: '封面链接1' },
    { id: 2, title: '书名2', author: '作者2', price: 60, stock: 200, cover: '封面链接2' },
]);

// 新书籍的信息
const newBook = ref({
    id: '',
    title: '',
    author: '',
    price: 0,
    stock: 0,
    cover: '',
});

// 控制对话框的可见性
const dialogVisible = ref(false);

// 显示对话框
const showDialog = () => {
    console.log('添加书目按钮被点击');
    dialogVisible.value = true;
};

// 添加书籍
const addBook = () => {
    if (newBook.value.id && newBook.value.title && newBook.value.author) {
        storageItems.value.push({ ...newBook.value }); // 添加新书籍
        newBook.value = { id: '', title: '', author: '', price: 0, stock: 0, cover: '' }; // 重置
        dialogVisible.value = false; 
    } else {
        alert('请填写所有字段');
    }
};

// 处理图片上传
const handleImageChange = (file) => {
    newBook.value.cover = URL.createObjectURL(file.raw);
};

// 限制上传文件类型
const beforeUpload = (file) => {
    const isImage = file.type.startsWith('image/');
    if (!isImage) {
        alert('请上传图片文件');
    }
    return isImage;
};
</script>

<style>
.storage {
    padding: 20px;
    font-size: 18px;
    text-align: left;
}

.storage-item {
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
}

.price-control {
    display: flex;
    align-items: center;
}

.price-control input {
    width: 80px;
    margin-left: 10px;
    text-align: center;
}

.upload-demo {
    margin-bottom: 20px;
}
</style>