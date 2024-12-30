<template>
    <div class="rightmain">
        <VantaBirds />
        <div class="righttop">
            <h3 class="topinfo">用户信息</h3>
        </div>
        <el-descriptions :border="true" column="1" class="userTable" size="large">
            <el-descriptions-item label="用户ID" label-width="100px">{{ store.userid }}</el-descriptions-item>
            <el-descriptions-item label="用户名">
                <span v-if="!isEditing.username">{{ store.username }}</span>
                <input v-if="isEditing.username" v-model="newUsername" type="text" />
                <el-button @click="toggleEdit('username')">{{ isEditing.username ? '保存' : '修改信息' }}</el-button>
            </el-descriptions-item>
            <el-descriptions-item label="地址">
                <span v-if="!isEditing.address">{{ store.address }}</span>
                <input v-if="isEditing.address" v-model="newAddress" type="text" />
                <el-button @click="toggleEdit('address')">{{ isEditing.address ? '保存' : '修改信息' }}</el-button>
            </el-descriptions-item>
            <el-descriptions-item label="余额">{{ store.balance }}
                <el-button id="recharge" @click="openPurchaseModal()">充值</el-button>
            </el-descriptions-item>
            <el-descriptions-item label="信用等级">{{ store.userlevel }}</el-descriptions-item>
        </el-descriptions>

        <el-dialog v-model="isModalOpen" title="账户充值">
            <div class="recharge-options">
                <el-button v-for="amount in rechargeAmounts" :key="amount" @click="setRechargeAmount(amount)">
                    {{ amount }}
                </el-button>
            </div>
            <div class="modal-actions">
                <span class="modal-buttons">
                    <el-button class='botbtn' @click="isModalOpen = false">取消</el-button>
                    <el-button class='botbtn' type="primary" @click="openQRcode">确认</el-button>
                </span>
            </div>
        </el-dialog>
        <el-dialog v-model="isQRcodeOpen" title="账户充值" @close="resetRecharge" class="QRcode-dia">
            <div class="qr-container">
                <el-avatar class="QRcode" shape="square" :size="90" :src="QRcode" alt="二维码" fit="cover" />
            </div>
            <div class="modal-actions">
                <el-button class='botbtn' @click="isQRcodeOpen = false">取消</el-button>
                <el-button class='botbtn' type="primary" @click="recharge">完成</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script lang="ts" setup>
import { ref, onBeforeUnmount } from 'vue';
import { mainStore } from '../../../store/index.ts';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import VantaBirds from '../../VantaBirds.vue';
import QRcode from '../../../assets/images/QRcode.jpg'
const store = mainStore();
const isEditing = ref({ username: false, address: false });
const newUsername = ref(store.username);
const newAddress = ref(store.address);
const isModalOpen = ref(false);
const isQRcodeOpen = ref(false);
const rechargeNum = ref(0);
const rechargeAmounts = [100, 200, 300, 500, 800, 1000];

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

const openPurchaseModal = () => {
    isModalOpen.value = true;
}

const openQRcode = () => {
    if (rechargeNum.value == 0) {
        ElMessage.error('请选择充值金额！');
    }
    else {
        isQRcodeOpen.value = true;
        isModalOpen.value = false;
    }
}

const setRechargeAmount = (amount: number) => {
    rechargeNum.value = amount;
}

const resetRecharge = () => {
    rechargeNum.value = 0; // 重置充值金额
}

const updateUserInfo = (field: 'username' | 'address', value: string) => {
    let formData = new FormData();
    formData.append('Uno', store.userid);
    formData.append('password', store.password);
    if (field === 'username') {
        store.username = value;
    } else {
        store.address = value;
    }
    formData.append('Uname', store.username);
    formData.append('address', store.address);

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
    formData.append('money', rechargeNum.value);
    axios.post(`${store.ip}/api/pre_pay`, formData, { headers: { 'Content-Type': 'multipart/form-data' } })
        .then(response => {
            let responseData = response.data;
            if (responseData.ret === 1) {
                ElMessage({ message: responseData.msg, type: 'error', duration: 5000 });
            } else {
                ElMessage.success('已成功充值' + rechargeNum.value + '元！');
                isQRcodeOpen.value = false;
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

.recharge-options {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
}

.modal-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

button {
    margin-left: 10px;
    background-color: aqua;
}

.modal-buttons {
    position: relative;
    margin-left: auto;
    margin-right: auto;
}

.QRcode {
    width: 370px;
    height: 370px;
}

.el-dialog {
    width: 800px;
    height: 500px;

}

.QRcode-dia {
    background-color: rgb(109, 117, 130);
}
.qr-container {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
    /* 增加二维码与下面按钮的边距 */
}

.modal-actions {
    display: flex;
    justify-content: center;
    /* 按钮居中对齐 */
    margin-top: 20px;
    /* 增加按钮与上面内容的边距 */
}
.botbtn {
    position: relative;
}
</style>