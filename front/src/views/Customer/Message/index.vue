<template>
    <div class="rightmain">
        <VantaBirds />
        <el-image style="width: 400px; height: 400px" class="vexlie2" fit="fit" :src="vexlieImg" />
        <div class="righttop">
            <h3 class="topinfo">留言</h3>
        </div>
        <div class="message">
            <el-input v-model="textarea" style="width: 90%; margin-left: 5%;" :autosize="{ minRows: 1, maxRows: 14 }" type="textarea" placeholder="请输入留言" />
            <el-button @click="sendMessage" class="sendMessageBtn">发送留言</el-button>



        </div>

    </div>
</template>

<script lang="ts" setup>
import { ref, onBeforeUnmount } from 'vue';
import { mainStore } from '../../../store/index.ts';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import VantaBirds from '../../VantaBirds.vue';
import vexlieImg from '../../../assets/images/vex_lie.png'
const store = mainStore();
const textarea = ref('');
const sendMessage = () => {
    let formData = new FormData();
    formData.append('Uno', store.userid);
    formData.append('message', textarea.value);
    axios({
        method: 'post',
        url: `${store.ip}/api/sendMsg`,
        data: formData,
        headers: { 'Content-Type': 'multipart/form-data' }
    }
    )
        .then(response => {
            let responseData = response.data;
            if (responseData.ret === 1) {
                ElMessage({ message: responseData.msg, type: 'error', duration: 5 * 1000, grouping: true });
            }
            else {
                ElMessage.success('留言发送成功');
                textarea.value = '';
            }
        });
}




</script>

<style scoped>
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
    color: black;
}

.topinfo {
    position: relative;
    width: 100%;
    height: 100%;
    align-items: center;
    font-size: 30px;
}

.message {
    flex-grow: 1;
    width: 90%;
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

button {
    margin-left: 10px;
    background-color: aqua;
}

.vexlie2 {
    position: absolute;
    right: 2%;
    bottom: -80px;
    width: 320px;
    height: 320px;
}
.sendMessageBtn {
    position: absolute;
    margin-left: 5%;
    bottom: 40%;
}
</style>