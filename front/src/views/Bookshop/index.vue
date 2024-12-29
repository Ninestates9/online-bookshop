<template>
    <div class="CustomerMain">
        <div class="leftmain">
            <div class="lefttop">
                <img :src="misakaImg" alt="Misaka Mikoto" />
                <strong>{{store.username}}</strong>
            </div>
            <div class="leftlist">
                <button id="Storage" class="leftbtn" @click="navigateTo('Storage')">库存</button>
                <button id="Order" class="leftbtn" @click="navigateTo('Order')">订单</button>
                <button id="Usermessage" class="leftbtn" @click="navigateTo('Usermessage')">消息</button>
                <button id="UserInfo" class="leftbtn" @click="navigateTo('UserInfo')">修改用户信息</button>
                <button id="MissingRecord" class="leftbtn" @click="navigateTo('MissingRecord')">缺书记录</button>
                <button id="MissingRecord" class="leftbtn" @click="navigateTo('Purchase')">采购单</button>
                <button id="MissingRecord" class="leftbtn" @click="navigateTo('Provider')">供应商</button>
                <button id="logout" class="leftbtn" @click="logout()">注销</button>
            </div>
        </div>
        <div class="rightmain">
            <router-view></router-view>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import misakaImg from '../../assets/images/vex.jpg';
import { mainStore } from '../../store/index.ts';
import { useRouter } from 'vue-router';
const store = mainStore();
const router = useRouter();

function navigateTo(componentName) {
    // 路由导航
    router.push({ name: componentName });

    // // 获取当前选中的按钮
    // let currentButton = document.getElementById(componentName);
    // const buttons = document.querySelectorAll('.nav-button'); // 假设按钮有类 'nav-button'

    // // 设置当前按钮的样式（例如背景颜色和文本颜色）
    // if (currentButton) {
    //     currentButton.style.backgroundColor = '#007bff'; // 设置选中的按钮背景色
    //     currentButton.style.color = '#ffffff'; // 设置选中按钮的文本颜色
    // }

    // // 重置其他按钮的样式
    // buttons.forEach(button => {
    //     if (button.id !== componentName) {
    //         button.style.backgroundColor = ''; // 重置为默认背景色
    //         button.style.color = ''; // 重置为默认文本颜色
    //     }
    // });
}
const logout = () => {
    router.push({path:'/SignIn'})
}
</script>

<style>
.CustomerMain {
    position: relative;
    width: 100vw;
    /* 修正为 100vw */
    height: 98.5vh;
    display: grid;
    grid-template-columns: 25% 75%;
}

.leftmain {
    position: relative;
    display: flex;
    background-color: rgba(255, 255, 255, 0);
    height: 98.5vh;
    width: 100%;
    display: grid;
    grid-template-rows: 15% 85%;
}

.lefttop {
    position: relative;
    display: flex;
    align-items: center;
    background-color: rgba(79, 0, 250, 0.421);
    width: 100%;
    height: 100%;
    overflow: hidden;
}

.lefttop strong {
    position: relative;
    display: flex;
    font-size: 20pt;
    margin-left: 10px;
    overflow: hidden;
}

.lefttop img {
    padding-left: 3%;
    height: 80%;
    border-radius: 10px;
}

.leftlist {
    position: relative;
    display: flex;
    align-items: center;
    background-color: rgba(5, 229, 222, 0.421);
    width: 100%;
    height: 100%;
    flex-direction: column
}

.leftbtn {
    background-color: rgba(163, 43, 218, 0.5);
    color: white;
    border: 1.5px solid rgba(176, 185, 15, 0.5);
    width: 100%;
    border-radius: 0px;
    margin-left: 0px;
}

.rightmain {
    position: relative;
    display: flex;
    height: 98.5vh;
    width: 100%;
    overflow: hidden;
    display: grid;
    grid-template-rows: 15% 85%;
}
</style>