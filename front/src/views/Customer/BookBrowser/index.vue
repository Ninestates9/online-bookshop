<template>
    <div class="rightmain">
      <div class="righttop">
        <div class="searchbox">
          <input
            type="text"
            class="search-input"
            placeholder="请输入搜索内容"
          />
          <button class="searchbtn" @click="performSearch">搜索</button>
        </div>
        <div class="search-options">
          <label v-for="option in searchOptions" :key="option.value">
            <input
              type="radio"
              name="searchOption"
              :value="option.value"
              v-model="selectedOption"
              @change="updateSearchOption"
            />
            {{ option.label }}
          </label>
        </div>
      </div>
      <div class="bookbrowser">
        <el-row :gutter="20">
          <el-col v-for="book in books" :key="book.id" :span="6">
            <el-card class="book-card">
              <img :src="book.cover" alt="书本封面" class="book-cover" />
              <div class="book-info">
                <h3>{{ book.title }}</h3>
                <p>作者: {{ book.author }}</p>
                <p>价格: ¥{{ book.price }}</p>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </div>
  </template>
  
  <script lang="ts" setup>
  import { ref } from 'vue';
  import { mainStore } from '../../../store/index.ts';
  import { ElCard, ElRow, ElCol } from 'element-plus';
  
  // 初始化 Pinia store
  const store = mainStore();
  
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
  
  const selectedOption = ref('bookId'); // 默认选中的值
  
  // 更新选中的搜索选项
  const updateSearchOption = () => {
    store.searchOP = selectedOption.value; // 保存到 store
    // alert(store.searchOP);
  };
  
  // 书籍数据
  const books = ref([
    { id: 1, title: '书名1', author: '作者1', price: 50, cover: '封面链接1' },
    { id: 2, title: '书名2', author: '作者2', price: 60, cover: '封面链接2' },
    { id: 3, title: '书名3', author: '作者3', price: 70, cover: '封面链接3' },
    // 更多书籍
  ]);
  
  // 搜索功能
  const performSearch = () => {
    console.log('搜索内容:', selectedOption.value);
    // 在这里添加搜索逻辑
  };
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
    flex-wrap: wrap; /* 允许换行 */
    margin-top: 10px; /* 添加顶部边距 */
  }
  
  .search-options label {
    margin-right: 10px; /* 添加右侧间距 */
    color: #333; /* 可根据需要调整颜色 */
  }
  
  .bookbrowser {
    position: relative;
    display: flex;
    align-items: center;
    background-color: rgba(233, 58, 5, 0.421);
    width: 100%;
    height: 100%;
    padding: 10px;
  }
  
  .book-card {
    max-width: 100%;
  }
  
  .book-cover {
    width: 100%;
    height: auto;
  }
  </style>