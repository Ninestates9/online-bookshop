<template>
    <div class="rightmain">
        <VantaBirds />
        <div class="righttop">
            <h3 class="topinfo">用户信息</h3>
        </div>
        <el-descriptions :border="true"  column="1" class="userTable" size="large">
            <el-descriptions-item label="用户ID" label-width="100px" >{{ store.userid }}</el-descriptions-item>
            <el-descriptions-item label="用户名" >
                <span v-if="!isEditing.username">{{ store.username }}</span>
                <input v-if="isEditing.username" v-model="newUsername" type="text" />
                <el-button @click="toggleEdit('username')">
                    {{ isEditing.username ? '保存' : '修改信息' }}
                </el-button>
            </el-descriptions-item>
            <el-descriptions-item label="地址">
                <span v-if="!isEditing.address">{{ store.address }}</span>
                <input v-if="isEditing.address" v-model="newAddress" type="text" />
                <el-button @click="toggleEdit('address')">
                    {{ isEditing.address ? '保存' : '修改信息' }}
                </el-button>
            </el-descriptions-item>
            <el-descriptions-item label="余额">{{ store.balance }}
                <el-button id="recharge" @click="recharge()">充值</el-button>
            </el-descriptions-item>
            <el-descriptions-item label="信用等级">{{ store.userlevel }}</el-descriptions-item>
        </el-descriptions>

    </div>
</template>

<script lang="ts" setup>
import { ref, onBeforeUnmount } from 'vue';
import { mainStore } from '../../../store/index.ts';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import VantaBirds from '../../VantaBirds.vue';
const store = mainStore();
const isEditing = ref({ username: false, address: false });
const newUsername = ref(store.username);
const newAddress = ref(store.address);

const toggleEdit = (field: 'username' | 'address') => {
    if (field === 'username') {
        isEditing.value.username = !isEditing.value.username;
        if (!isEditing.value.username) {
            updateUserInfo('username', newUsername.value);
        }
    } else if (field === 'address') {
        isEditing.value.address = !isEditing.value.address;
        if (!isEditing.value.address) {
            updateUserInfo('address', newAddress.value);
        }
    }
};

const updateUserInfo = (field: 'username' | 'address', value: string) => {
    let formData = new FormData();
    formData.append('Uno', store.userid);
    formData.append('password', store.password);
    if (field === 'username') {
        store.username = value;
        formData.append('Uname', value);
    } else {
        store.address = value;
        formData.append('address', value);
    }

    axios.post(`${store.ip}/api/updateInfo`, formData, { headers: { 'Content-Type': 'multipart/form-data' } })
        .then(response => {
            let responseData = response.data;
            if (responseData.ret === 1) {
                ElMessage({ message: responseData.msg, type: 'error', duration: 5000 });
            }
        });
};

const recharge = () => {
    let formData = new FormData();
    formData.append('Uno', store.userid);
    formData.append('money', 100);
    axios.post(`${store.ip}/api/pre_pay`, formData, { headers: { 'Content-Type': 'multipart/form-data' } })
        .then(response => {
            let responseData = response.data;
            if (responseData.ret === 1) {
                ElMessage({ message: responseData.msg, type: 'error', duration: 5000 });
            } else {
                getUserInfo();
            }
        });
};

const getUserInfo = () => {
    let formdata = new FormData();
    formdata.append('Uno', store.userid);
    axios.post(`${store.ip}/api/getInfo`, formdata, { headers: { 'Content-Type': 'multipart/form-data' } })
        .then(response => {
            let responseData = response.data;
            store.setUserId(responseData.info.Uno);
            store.username = responseData.info.Uname;
            store.userlevel = responseData.info.level;
            store.address = responseData.info.address;
            store.balance = responseData.info.balance;
        })
        .catch(error => {
            console.error('Error posting data:', error);
            ElMessage({ message: '网络错误，请稍后重试！', type: 'error', duration: 5000 });
        });
};

onBeforeUnmount(() => {
    getUserInfo();
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
    background-color: rgba(255, 255, 255, 0);
    width: 100%;
    height: 100%;
}

.topinfo {
    position: relative;
    width: 100%;
    height: 100%;
    align-items: center;
    font-size: 30px;
}

.userTable {
    width: 50%;
    margin-left: auto;
    margin-right: auto;
}

.el-descriptions {
    padding: 20px;
    font-size: 18px;
    text-align: left;
}

button {
    margin-left: 10px;
    background-color: aqua;
}
</style>