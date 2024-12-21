<template>
        <div class="rightmain">
            <div class="righttop">
                <div class="searchbox">
                    <input type="text" class="search-input" />
                    <button class="searchbtn">搜索</button>
                </div>
                <div class="righttool">
                    <svg t="1734526169153" class="icon" viewBox="0 0 1160 1024" version="1.1"
                        xmlns="http://www.w3.org/2000/svg" p-id="4240" width="200" height="200">
                        <path
                            d="M415.1296 857.429333a83.285333 83.285333 0 1 1 0 166.570667 83.285333 83.285333 0 0 1 0-166.570667z m499.643733 0a83.285333 83.285333 0 1 1 0 166.570667 83.285333 83.285333 0 0 1 0-166.570667zM213.435733 0v0.4096l5.12-0.034133a34.133333 34.133333 0 0 1 34.2016 29.2864l20.48 143.803733h834.013867a34.133333 34.133333 0 0 1 33.6896 39.697067l-83.524267 506.88a68.266667 68.266667 0 0 1-67.345066 57.1392H318.327467c-1.774933 0-3.515733-0.136533-5.2224-0.375467h-6.144a34.133333 34.133333 0 0 1-34.2016-29.2864L197.188267 218.043733l-7.338667-44.578133h0.989867l-12.868267-90.2144H20.48V0h192.955733z m330.308267 340.138667H481.28v270.404266h62.464V340.138667z m312.285867 0h-62.464v270.404266h62.464V340.138667z"
                            fill="#515151" p-id="4241"></path>
                    </svg>
                </div>
            </div>
            <div class="bookbrowser"></div>
        </div>

</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { mainStore } from '../../../store/index.ts';

// 初始化 Pinia store
const store = mainStore();
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
    background-color: rgba(91, 247, 1, 0.421);
    width: 100%;
    height: 100%;
    display: grid;
    grid-template-columns: 85% 15%;
}

.searchbox {
    position: relative;
    display: flex;
    align-items: center;
    background-color: rgba(91, 247, 1, 0.421);
    width: 100%;
    height: 100%;
    padding: 10px;
    overflow: hidden;
    /* 添加内边距 */
}

.search-input {
    width: 80%;
    /* 设置宽度为100% */
    padding: 10px;
    /* 添加内边距 */
    margin-left: 3%;
    border: 1px solid #ccc;
    /* 边框样式 */
    border-radius: 4px;
    /* 圆角 */
}

.searchbtn {
    background-color: rgba(163, 43, 218, 0.5);
    color: white;
    border: 1.5px solid rgba(176, 185, 15, 0.5);
    max-height: 100%;
    margin-right: 5px;
}

.righttool {
    position: relative;
    justify-items: center;
    align-items: center;
    display: flex;
    background-color: rgba(255, 255, 255, 0);
    height: 100%;
    width: 100%;
    overflow: hidden;
}

.righttool svg {
    position: relative;
    margin-left: 30%;
    max-width: 40%;
    max-height: 40%;
    cursor: pointer;
}

.bookbrowser {
    position: relative;
    display: flex;
    align-items: center;
    background-color: rgba(233, 58, 5, 0.421);
    width: 100%;
    height: 100%;
}
</style>