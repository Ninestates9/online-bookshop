<template>
  <div class="rightmain">
      <div class="righttop">
          <h3 class="topinfo">历史订单</h3>
      </div>
      <div class="history">

      </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { mainStore } from '../../../store/index.ts';
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

.history {
  padding: 20px;
  font-size: 18px;
  text-align: left; /* 确保文本左对齐 */
}


button {
  margin-left: 10px;
}
</style>