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
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { mainStore } from '../../../store/index.ts';

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
};
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
    text-align: left; /* 确保文本左对齐 */
}

.userinfo p {
    margin: 5px 0;
}

button {
    margin-left: 10px;
}
</style>