<template>
    <div class="rightmain">
        <div class="righttop">
            <h3 class="topinfo">供应商</h3>
        </div>
        <div class="Provider">
            <button @click="dialogVisible = true">添加供应商</button>
            <div v-for="(vendor, index) in provider" :key="vendor.Vno" class="vendor-item">
                <h4>{{ vendor.Vname }}</h4>
                <p>地址: {{ vendor.Vaddress }}</p>
                <h5>供应的书籍:</h5>
                <ul>
                    <li v-for="book in vendor.books" :key="book.Bno">
                        {{ book.Bname }} (书号: {{ book.Bno }}, 丛书号: {{ book.Bsubno }}, 状态: {{ book.state }})
                    </li>
                </ul>
            </div>
        </div>

        <!-- 对话框 -->
        <el-dialog :model-value="dialogVisible" title="添加供应商">
            <el-form :model="newVendor">
                <el-form-item label="供应商名称" required>
                    <el-input v-model="newVendor.Vname" />
                </el-form-item>
                <el-form-item label="地址" required>
                    <el-input v-model="newVendor.Vaddress" />
                </el-form-item>
                <el-form-item label="书籍">
                    <el-input v-model="newBook.Bno" placeholder="书号" />
                    <el-input type="number" v-model="newBook.Bsubno" placeholder="丛书号" />
                    <el-input v-model="newBook.state" placeholder="状态" />
                    <el-button @click="addBook">添加书籍</el-button>
                    <ul>
                        <li v-for="(book, index) in newVendor.books" :key="index">
                         书号: {{ book.Bno }}, 丛书号: {{ book.Bsubno }}, 状态: {{ book.state }}
                            <el-button @click="removeBook(index)">删除</el-button>
                        </li>
                    </ul>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="addProvider">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { mainStore } from '../../../store/index.ts';
import axios from 'axios';
import { ElMessage } from 'element-plus';

const store = mainStore();
const provider = ref([]);
const dialogVisible = ref(false);
const newVendor = ref({ Vname: '', Vaddress: '', books: [] });
const newBook = ref({ Bname: '', Bno: '', Bsubno: 0, state: '' });

const getProvider = () => {
    axios.post(`${store.ip}/api/getVendors`, { headers: { 'Content-Type': 'multipart/form-data' } })
        .then(response => {
            if (response.data.ret === 0) {
                provider.value = response.data.vendors || [];
            } else {
                ElMessage.error(response.data.msg);
            }
        })
        .catch(error => {
            console.error('Error fetching vendors:', error);
            ElMessage.error('网络错误，请稍后重试！');
        });
}

const addProvider = () => {
    let formData = new FormData();
    formData.append('Vname', newVendor.value.Vname);
    formData.append('Vaddress', newVendor.value.Vaddress);
    formData.append('books', JSON.stringify(newVendor.value.books));

    axios.post(`${store.ip}/api/addVendor`, formData, { headers: { 'Content-Type': 'multipart/form-data' } })
        .then(response => {
            if (response.data.ret === 0) {
                provider.value.push(response.data.vendor);
                ElMessage.success('供应商添加成功');
                dialogVisible.value = false;
                resetVendor();
            } else {
                ElMessage.error(response.data.msg);
            }
        })
        .catch(error => {
            console.error('Error adding vendor:', error);
            ElMessage.error('网络错误，请稍后重试！');
        });
}

const addBook = () => {
    if (newBook.value.Bname && newBook.value.Bno) {
        newVendor.value.books.push({ ...newBook.value });
        resetBook();
    } else {
        ElMessage.warning('请填写书名和书号');
    }
}

const removeBook = (index) => {
    newVendor.value.books.splice(index, 1);
}

const resetVendor = () => {
    newVendor.value = { Vname: '', Vaddress: '', books: [] };
}

const resetBook = () => {
    newBook.value = { Bname: '', Bno: '', Bsubno: 0, state: '' };
}

onMounted(() => {
    getProvider();
});
</script>

<style>
.rightmain {
    position: relative;
    display: flex;
    height: 98.5vh;
    width: 100%;
    overflow: hidden;
    display: grid;
    grid-template-rows: 15% 85%;
}

.righttop {
    position: relative;
    overflow: hidden;
    align-items: center;
    background-color: rgba(91, 247, 1, 0.421);
    width: 100%;
    height: 100%;
}

.topinfo {
    position: relative;
    width: 100%;
    height: 100%;
    align-items: center;
    font-size: 50px;
}

.Provider {
    padding: 20px;
    font-size: 18px;
    text-align: left;
    overflow-y: auto;
    /* 确保文本左对齐 */
}


button {
    margin-left: 10px;
}
button {
  background-color: aqua;
}
.vendor-item {
    margin-bottom: 20px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #f9f9f9;
    color: black;
}

.vendor-item h4 {
    margin: 0;
    font-size: 20px;
}

.vendor-item p {
    margin: 5px 0;
}

.vendor-item ul {
    list-style-type: none;
    padding: 0;
}

.vendor-item li {
    margin: 5px 0;
}
</style>