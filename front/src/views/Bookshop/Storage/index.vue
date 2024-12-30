<template>
    <div class="m-storage-rightmain">
        <div class="m-righttop">
            <h3 class="topinfo">库存</h3>
        </div>
        <el-scroller class="storage">
            <el-card @click="openPurchaseModal(book)" v-for="(book, index) in storageItems" :key="book.Bno"
                class="book-card">
                <div class="m-book-info">
                    <img :src="`${store.ip}/cover/${book.cover}`" alt="书本封面" class="book-cover" />
                    <div class="m-book-details">
                        <div class="m-book-left">
                            <div style="font-weight: bold;">{{ book.Bname }}</div>
                            <div>作者: {{ book.authors.join(' ') }}</div>
                            <div>出版社: {{ book.press }}</div>
                        </div>
                        <div class="m-book-right">
                            <div>价格: {{ book.price }}</div>
                            <div>库存量: {{ book.quantity }}</div>
                        </div>
                    </div>
                </div>
            </el-card>
            <el-dialog v-model="isModalOpen" title="书籍详情">
                <el-descriptions :border="true" column="3" size="large">
                    <el-descriptions-item :rowspan="5" :width="200" label="" label-width="0px" align="center">
                        <img :src="store.ip + '/cover/' + selectedBook?.cover" alt="书本封面" class="book-cover" />
                    </el-descriptions-item>
                    <el-descriptions-item label="书号"> {{ selectedBook?.Bno }}</el-descriptions-item>
                    <el-descriptions-item label="丛书号">{{ selectedBook?.Bsubno }}</el-descriptions-item>
                    <el-descriptions-item label="书名">{{ selectedBook?.Bname }}</el-descriptions-item>
                    <el-descriptions-item label="作者">{{ selectedBook?.authors.join(' ') }}</el-descriptions-item>
                    <el-descriptions-item label="关键字">{{ selectedBook?.keys.join(' ') }}</el-descriptions-item>
                    <el-descriptions-item label="出版社">{{ selectedBook?.press }}</el-descriptions-item>
                    <el-descriptions-item label="库存">{{ selectedBook?.quantity }}</el-descriptions-item>
                    <el-descriptions-item label="位置"> {{ selectedBook?.position }}</el-descriptions-item>
                    <el-descriptions-item label="目录">{{ selectedBook?.catalog }}</el-descriptions-item>


                </el-descriptions>
                <div class="m-footer">
                    <div class="price-control">
                        <label>价格: ¥</label>
                        <input type="number" v-model.number="selectedBook.price" min="0" />
                        <el-button size="default" @click="updatePrice(selectedBook)">更新价格</el-button>
                    </div>
                    <el-button @click="isModalOpen = false">关闭</el-button>
                    <el-button @click="deleteBook(selectedBook.Bno, selectedBook.Bsubno)"
                        class="deleteBtn">删除图书</el-button>
                </div>
            </el-dialog>
        </el-scroller>

        <!-- 添加书目按钮 -->
        <div class="add-button-container">
            <el-button size="large" type="primary" @click="showDialog">添加书目</el-button>
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
import { ElCard, ElRow, ElCol, ElMessage } from 'element-plus';

const store = mainStore();

// 存储书籍数据
const storageItems = ref([]);
const isModalOpen = ref(false);
const selectedBook = ref(null);
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
    isModalOpen.value = true;
};
// 显示对话框
const showDialog = () => {
    dialogVisible.value = true;
};

const deleteBook = (Bno, Bsubno) => {
    let formData = new FormData();
    formData.append('Bno', Bno);
    formData.append('Bsubno', Bsubno);
    axios({
        method: 'post',
        url: `${store.ip}/api/deleteBook`,
        data: formData,
        headers: { 'Content-Type': 'multipart/form-data' },
    })
        .then((response) => {
            const responseData = response.data;
            if (responseData.ret === 1) {
                ElMessage({
                    message: responseData.msg,
                    type: 'error',
                    duration: 5 * 1000,
                    grouping: true,
                });
            } else {
                // alert(responseData.ret);
                getBooks();
            }
        })
}

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
.m-storage-rightmain {
    display: flex;
    flex-direction: column;
    height: 100vh;
    width: 100%;
    justify-content: center;
    align-items: center;
}

.m-righttop {
    font-size: 30px;
}

.storage {
    display: flex;
    flex-wrap: wrap;
    overflow-y: auto;
    width: 100%;
    flex-grow: 1;
}



.book-card {
    flex: 0 1 calc(23% - 8px);
    /* 每个卡片占据三分之一的宽度，减去边距 */
    display: flex;
    flex-direction: column;
    /* 垂直排列内容 */
    justify-content: space-between;
    /* 内容均匀分布 */
    height: 450px;
    /* 固定高度 */
    margin: 5px;
    /* 卡片之间的间距 */
    border-radius: 8px;
    /* 圆角 */
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    /* 阴影效果 */
    box-sizing: border-box;
    /* 包含边距和填充在宽高内 */
    cursor: pointer;
}

.book-cover {
    width: 100%;
    /* 充满宽度 */
    height: 300px;
    /* 固定高度 */
    object-fit: cover;
    /* 保持比例并覆盖 */
}

.price-control {
    display: flex;
    align-items: stretch;
    margin-top: 5px;
    width: 60%;
    justify-content:center;
    font-size: large;
}

.price-control input {
    width: 80px;
    margin-left: 5%;
    margin-right: 5%;
    text-align: center;
    font-size: large;
}

.m-book-info {
    display: flex;
    flex-direction: column;
}

.m-book-left {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.m-book-right {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
}

.m-book-details {
    margin-top: 10%;
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
}

.add-button-container {
    padding: 20px;
    text-align: center;
    margin-bottom: 5%;
}

.upload-demo {
    margin-bottom: 20px;
}

button {
    background-color: aqua;
}

.m-footer {
    margin-top: 5%;
    margin-bottom: 5%;
    display: flex;
    align-items: center;
    justify-content: space-around;
}

</style>