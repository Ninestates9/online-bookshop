<template>
    <div class="rightmain">
        <div class="righttop">
            <h3 class="topinfo">用户信息</h3>
        </div>
        <div class="userinfo">
            <p>
                <strong>用户ID:</strong> {{ store.userid }}
            </p>
            <p>
                <strong>用户名:</strong>
                <span v-if="!isEditing.username">{{ store.username }}</span>
                <input v-if="isEditing.username" v-model="newUsername" type="text" />
                <button @click="toggleEdit('username')">
                    {{ isEditing.username ? '保存' : '修改信息' }}
                </button>
            </p>
            <p>
                <strong>地址:</strong>
                <span v-if="!isEditing.address">{{ store.address }}</span>
                <input v-if="isEditing.address" v-model="newAddress" type="text" />
                <button @click="toggleEdit('address')">
                    {{ isEditing.address ? '保存' : '修改信息' }}
                </button>
            </p>
            <p>
                <strong>余额:</strong> {{ store.balance }}
            </p>
            <p>
                <strong>信用等级:</strong> {{ store.userlevel }}
            </p>
            <button id="recharge" @click="recharge()">充值</button>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, onBeforeUnmount, onMounted } from 'vue';
import { mainStore } from '../../../store/index.ts';
import axios from 'axios';
import { ElMessage } from 'element-plus';

const store = mainStore();
const isEditing = ref({ username: false, address: false });
const newUsername = ref(store.username);
const newAddress = ref(store.address);

const toggleEdit = (field: 'username' | 'address') => {
    if (field === 'username') {
        isEditing.value.username = !isEditing.value.username;
        if (!isEditing.value.username) {
            // 这里可以调用接口保存修改后的用户名
            store.username = newUsername.value;

        }
    } else if (field === 'address') {
        isEditing.value.address = !isEditing.value.address;
        if (!isEditing.value.address) {
            // 这里可以调用接口保存修改后的地址
            store.address = newAddress.value;

        }
    }
    let formData = new FormData();
            formData.append('Uno', store.userid);
            formData.append('password', store.password);
            formData.append('Uname', store.username);
            formData.append('address', store.address);

            axios({
                method: 'post',
                url: `${store.ip}/api/updateInfo`,
                data: formData,
                headers: { 'Content-Type': 'multipart/form-data' }
            }
            )
                .then(response => {
                    let responseData = response.data;
                    if (responseData.ret === 1) {
                        ElMessage({ message: responseData.msg, type: 'error', duration: 5 * 1000, grouping: true });
                    }
                })
};

onBeforeUnmount(()=>{
    getuserinfo();
});


const recharge = () => {
    let formData = new FormData();
            formData.append('Uno', store.userid);
            formData.append('money', 100);
            axios({
                method: 'post',
                url: `${store.ip}/api/pre_pay`,
                data: formData,
                headers: { 'Content-Type': 'multipart/form-data' }
            }
            )
                .then(response => {
                    let responseData = response.data;
                    if (responseData.ret === 1) {
                        ElMessage({ message: responseData.msg, type: 'error', duration: 5 * 1000, grouping: true });
                    }
                    else{
                        getuserinfo();
                    }
                })
}


const getuserinfo = () => {
    let formdata = new FormData();
    formdata.append('Uno', store.userid)
    axios({
        method: 'post',
        url: `${store.ip}/api/getInfo`,
        data: formdata,
        headers: { 'Content-Type': 'multipart/form-data' }
    }
    )
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
            ElMessage({ message: '网络错误，请稍后重试！', type: 'error', duration: 5 * 1000, grouping: true });
        });
}
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

.userinfo {
    padding: 20px;
    font-size: 18px;
    text-align: left;
    /* 确保文本左对齐 */
}

.userinfo p {
    margin: 5px 0;
}

button {
    margin-left: 10px;
}
button {
  background-color: aqua;
}
</style>