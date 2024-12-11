<template>
    <div class="container">
        <img src="../../assets/images/sign_background.jpg">
        <div class="signin-wrapper">
            <h1 class="header">
                注册
            </h1>
            <div class="form-wrapper">
                <h2 class="input-title">用户名</h2>
                <input type="text" v-model="username" placeholder="请输入用户名" class="input-item">
                <h2 class="input-title">密码</h2>
                <input type="password" v-model="password1" placeholder="请输入密码" class="input-item">
                <h2 class="input-title">确认密码</h2>
                <input type="password" v-model="password2" placeholder="请再次输入密码" class="input-item">
                <button @click="check()" class="btn">
                    注册
                </button>
            </div>
            <div class="msg">
                已有账户？
                <router-link to="/SignIn" class="link">立即登录</router-link>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
import axios from 'axios';
import { mainStore } from '../../store/index.ts';
import router from "../../router";

const store = mainStore();
const username = ref('');
const password1 = ref('');
const password2 = ref('');

const check = () => {
    if (username.value === '' || password1.value === '' || password2.value === '') {
        ElMessage({message: '用户名和密码不能为空', type: 'error', duration: 5 * 1000, grouping: true});
        return;
    }

    if (/^\s*$/.test(username.value)) {
        ElMessage({message: '用户名不能为空格', type: 'error', duration: 5 * 1000, grouping: true});
        return;
    }

    if (password1.value.length < 6 || password1.value.length > 24) {
        ElMessage({message: '密码长度必须为6-24位', type: 'error', duration: 5 * 1000, grouping: true});
        return;
    }

    console.log('password1:', password1);
    console.log('password2:', password2);

    if (password1.value !== password2.value) {
        ElMessage({message: '输入密码不一致', type: 'error', duration: 5 * 1000, grouping: true});
    }
    else {
        signUp();
    }
}

const signUp = () => {
    let formData = new FormData();
    formData.append('username', username.value);
    formData.append('password', password1.value);

    axios({
        method: 'post', 
        url: `${store.ipAddress}/api/signUp`, 
        data: formData, 
        headers:{'Content-Type': 'multipart/form-data'}}
    )
    .then(response => {
        let responseData = response.data;
        if (responseData.ret === 0) {
        store.setUsername(username.value);
        localStorage.setItem('username', username.value);
        router.push({path:'/'})
        } else if(responseData.ret === 1) {
        ElMessage({message: '注册失败：' + responseData.msg, type: 'error', duration: 5 * 1000, grouping: true});
        }
    })
    .catch(error => {
        console.error('Error posting data:', error);
        ElMessage({message: '注册失败：网络错误，请稍后重试！', type: 'error', duration: 5 * 1000, grouping: true});
    });
}
</script>

<style scoped>
    .container {
        height: 100vh;
    }
    img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center;
        position: fixed;
        z-index: -1;
    }
    .signin-wrapper {
        background-color: rgba(136, 169, 202, 0.8); 
        width: 358px;
        height: 628px;
        border-radius: 15px;
        padding: 0 50px;
        display: flex;
        flex-direction: column;
        position: relative;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        backdrop-filter: blur(5px);
    }
    .header {
        opacity: 0.7;
        font-size: 38px;
        font-weight: bold;
        text-align: center;
        margin-top: 60px;
        margin-bottom: 40px;
        color: #ffffff;
    }
    .input-title {
        opacity: 0.7;
        font-size: 18px;
        color: #ffffff;
    }
    .input-item {
        opacity: 0.7;
        display: block;
        width: 100%;
        height: 35px;
        margin-bottom: 20px;
        border: 0;
        padding: 2px;
        padding-left: 10px;
        font-size: 18px;
        outline: none;
        background-color: #577594;
        color: #f8f8f8;
        border-radius: 10px;
        border: 2px solid transparent;
        transition: border-color 0.2s ease;
    }
    .input-item:hover,
    .input-item:focus {
        border-color: #66a1cb;
    }
    .input-item::placeholder {
        color: #c3c3c3;
    }
    .btn {
        opacity: 0.7;
        text-align: center;
        outline: none;
        padding: 10px;
        width: 100%;
        margin-top: 40px;
        background-color: #334e68;
        color: #fff;
    }
    .link {
        opacity: 0.9;
        color: #04073d;
    }
    .msg {
        opacity: 0.7;
        text-align: center;
        line-height: 88px;
        color: #eeeeee;
    }
</style>