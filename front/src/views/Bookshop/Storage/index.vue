<template>
    <div class="rightmain">
        <div class="righttop">
            <h3 class="topinfo">库存</h3>
        </div>
        <div class="storage">
            <div v-for="(book, index) in storageItems" :key="book.Bno" class="storage-item">
                <img :src="`${store.ip}/cover/${book.cover}`" alt="书本封面" class="book-cover" />
                <div class="book-details">
                    <div class="basic-details">
                        <p>书号: {{ book.Bno }}</p>
                        <p>丛书号: {{ book.Bsubno }}</p>
                        <h4>{{ book.Bname }}</h4>
                        <p>作者: {{ book.authors.join(', ') }}</p>
                        <p>关键字: {{ book.keys.join(', ') }}</p>
                        <p>出版社: {{ book.press }}</p>
                        <div class="price-control">
                            <label>价格: ¥</label>
                            <input type="number" v-model.number="book.price" min="0" />
                            <el-button size="small" @click="updatePrice(book)">更新价格</el-button>
                        </div>

                        <p>库存量: {{ book.quantity }}</p>
                        <p>目录: {{ book.catalog }}</p>
                        <p>位置: {{ book.position }}</p>
                    </div>
                </div>
            </div>
            <el-button type="primary" @click="showDialog">添加书目</el-button>
        </div>

        <el-dialog title="添加新书籍" :model-value="dialogVisible">
            <div>
                <el-upload class="upload-demo" action="#" :show-file-list="false" :on-change="handleImageChange"
                    :before-upload="beforeUpload" accept="image/*">
                    <el-button size="small" type="primary">上传封面图</el-button>
                </el-upload>

                <el-form :model="newBook" label-width="80px">
                    <el-form-item label="书号">
                        <el-input v-model="newBook.Bno" placeholder="书号"></el-input>
                    </el-form-item>

                    <el-form-item label="丛书号">
                        <el-input v-model.number="newBook.Bsubno" type="number" placeholder="丛书号"></el-input>
                    </el-form-item>

                    <el-form-item label="书名">
                        <el-input v-model="newBook.Bname" placeholder="书名"></el-input>
                    </el-form-item>

                    <el-form-item label="作者">
                        <el-input v-model="newBook.authors" placeholder="作者" type="textarea"></el-input>
                    </el-form-item>

                    <el-form-item label="关键字">
                        <el-input v-model="newBook.keys" placeholder="关键字" type="textarea"></el-input>
                    </el-form-item>

                    <el-form-item label="出版社">
                        <el-input v-model="newBook.press" placeholder="出版社"></el-input>
                    </el-form-item>

                    <el-form-item label="价格">
                        <el-input v-model.number="newBook.price" type="number" placeholder="价格"></el-input>
                    </el-form-item>

                    <el-form-item label="库存量">
                        <el-input v-model.number="newBook.quantity" type="number" placeholder="库存量"></el-input>
                    </el-form-item>

                    <el-form-item label="目录">
                        <el-input v-model="newBook.catalog" placeholder="目录"></el-input>
                    </el-form-item>

                    <el-form-item label="位置">
                        <el-input v-model.number="newBook.position" type="number" placeholder="位置"></el-input>
                    </el-form-item>
                </el-form>
            </div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="addBook">确 定</el-button>
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

// 存储书籍数据
const storageItems = ref([]);

// 新书籍的信息
const newBook = ref({
    Bno: '',
    Bsubno: 0,
    Bname: '',
    authors: [''],
    keys: [''],
    press: '',
    price: 0,
    quantity: 0,
    catalog: '',
    position: 0,
    cover: null, // 用于存储封面图文件
});

// 控制对话框的可见性
const dialogVisible = ref(false);

// 显示对话框
const showDialog = () => {
    dialogVisible.value = true;
};

// 更新价格
const updatePrice = async (book) => {
    let formData = new FormData();
    formData.append('Bno', book.Bno);
    formData.append('Bsubno', String(book.Bsubno));
    formData.append('price', String(book.price));

    // 发送请求更新价格
    axios({
        method: 'post',
        url: `${store.ip}/api/updatePrice`,
        data: formData,
        headers: { 'Content-Type': 'multipart/form-data' },
    })
        .then((response) => {
            let responseData = response.data;
            if (responseData.ret === 1) {
                ElMessage({
                    message: responseData.msg,
                    type: 'error',
                    duration: 5 * 1000,
                    grouping: true,
                });
            } else {
                ElMessage({
                    message: '价格更新成功',
                    type: 'success',
                    duration: 5 * 1000,
                    grouping: true,
                });
                getBooks();
            }
        })
        .catch((error) => {
            console.error('更新价格失败:', error);
            ElMessage({
                message: '更新价格失败，请稍后重试！',
                type: 'error',
                duration: 5 * 1000,
                grouping: true,
            });
        });
};

// 获取所有图书数据
const getBooks = () => {
    axios({
        method: 'post',
        url: `${store.ip}/api/getBooks`,
        headers: { 'Content-Type': 'multipart/form-data' },
    })
        .then((response) => {
            const responseData = response.data;
            if (responseData.ret === 0) {
                // 更新存储的书籍数据
                storageItems.value = responseData.books.map((book) => ({
                    Bno: book.Bno,
                    Bsubno: book.Bsubno,
                    Bname: book.Bname,
                    authors: book.authors,
                    keys: book.keys,
                    press: book.press,
                    price: book.price,
                    quantity: book.quantity,
                    cover: book.cover,
                    catalog: book.catalog,
                    position: book.position,
                }));
            } else {
                alert('获取书籍数据失败: ' + responseData.msg);
            }
        })
        .catch((error) => {
            console.error('获取书籍数据失败:', error);
            alert('获取书籍数据失败，请稍后重试！');
        });
};

// 添加书籍
const addBook = async () => {
    // 创建 FormData 对象
    const formData = new FormData();

    formData.append('Bno', newBook.value.Bno);
    formData.append('Bsubno', String(newBook.value.Bsubno));
    formData.append('Bname', newBook.value.Bname);
    formData.append('authors', newBook.value.authors);
    formData.append('keys', newBook.value.keys);
    formData.append('press', newBook.value.press);
    formData.append('price', String(newBook.value.price));
    formData.append('quantity', String(newBook.value.quantity));
    formData.append('catalog', newBook.value.catalog);
    formData.append('position', String(newBook.value.position));

    if (newBook.value.cover) {
        formData.append('cover', newBook.value.cover); // 添加封面图文件
    }

    axios({
        method: 'post',
        url: `${store.ip}/api/addBooks`,
        data: formData,
        headers: { 'Content-Type': 'multipart/form-data' },
    })
        .then((response) => {
            let responseData = response.data;
            if (responseData.ret === 1) {
                ElMessage({
                    message: responseData.msg,
                    type: 'error',
                    duration: 5 * 1000,
                    grouping: true,
                });
            } else {
                getBooks();
            }
        });
};

// 处理图片上传
const handleImageChange = (file) => {
    newBook.value.cover = file.raw; // 存储封面图文件
};

// 限制上传文件类型
const beforeUpload = (file) => {
    const isImage = file.type.startsWith('image/');
    if (!isImage) {
        alert('请上传图片文件');
    }
    return isImage;
};

// 组件加载时获取图书数据
onMounted(() => {
    getBooks();
});
</script>

<style scoped>
.storage {
    padding: 20px;
    font-size: 18px;
    text-align: left;
    overflow-y: auto;
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