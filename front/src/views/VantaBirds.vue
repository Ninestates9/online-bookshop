<script>
import { onMounted, onBeforeUnmount, ref } from 'vue';
import * as THREE from 'three'; // 导入 Three.js
import BIRDS from 'vanta/src/vanta.birds'; // 导入动态样式逻辑

export default {
  setup() {
    // 使用 `ref` 创建响应式 DOM 引用
    const vantaRef = ref(null);
    let vantaEffect = null;

    // 在组件挂载时初始化 Vanta 动画
    onMounted(() => {
      vantaEffect = BIRDS({
        el: vantaRef.value, // 使用 Vue 3 的 `ref` 值
        THREE: THREE,
        mouseControls: true,
        touchControls: true,
        gyroControls: false,
        minHeight: 200.0,
        minWidth: 200.0,
        scale: 1.0,
        backgroundColor: 0xffffff,
        color1: 14381274,
        color2: 16443110,
      });
    });

    // 在组件卸载前销毁 Vanta 动画
    onBeforeUnmount(() => {
      if (vantaEffect) {
        vantaEffect.destroy();
        vantaEffect = null;
      }
    });

    return {
      vantaRef,
    };
  },
};
</script>

<template>
  <!-- 将 ref 绑定到 div -->
  <div ref="vantaRef" style="width: 100%; height: 100vh"></div>
</template>