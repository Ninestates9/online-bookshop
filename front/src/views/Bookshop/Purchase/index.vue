<template>
    <div class="rightmain">
      <div class="righttop">
        <h3 class="topinfo">采购单</h3>
      </div>
      <div class="purchase">
        <!-- Loop through purchase orders and display them -->
        <div v-if="purchaseList.length > 0" class="purchase-list">
          <div v-for="(purchase, index) in purchaseList" :key="index" class="purchase-item">
            <p><strong>采购单号:</strong> {{ purchase.Pno }}</p>
            <p><strong>订单号集:</strong> {{ purchase.SnoSet.join(', ') }}</p>
            <button @click="completePurchase(purchase.Pno)">完成采购单</button>
            <hr />
          </div>
        </div>
        <div v-else>
          <p>暂无采购单。</p>
        </div>
      </div>
    </div>
  </template>
  
  
  <script lang="ts" setup>
  import { ref, onMounted } from 'vue';
  import { mainStore } from '../../../store/index.ts';
  import axios from 'axios';
  import { ElMessage } from 'element-plus';
  
  const store = mainStore();
  const purchaseList = ref<any[]>([]);  // To store the purchase orders
  
  // Function to get purchase orders from the API
  const getPurchaseOrders = () => {
    axios({
      method: 'post',
      url: `${store.ip}/api/getPurchase`,  // Make sure this is the correct endpoint
      headers: { 'Content-Type': 'application/json' },
    })
      .then((response) => {
        let responseData = response.data;
        if (responseData.ret === 1) {
          ElMessage({
            message: responseData.msg,
            type: 'error',
            duration: 5 * 1000,
          });
        } else {
          purchaseList.value = responseData.purchase || [];  // Update the purchaseList
        }
      })
      .catch((error) => {
        console.error('获取采购单失败:', error);
        ElMessage.error('获取采购单失败，请稍后重试！');
      });
  };
  
  // Function to complete a purchase order
  const completePurchase = (Pno: number) => {
    const formData = new FormData();
    formData.append('Pno', Pno.toString());
  
    // Sending the data via multipart/form-data
    axios({
      method: 'post',
      url: `${store.ip}/api/finishPurchase`,  // Make sure this is the correct endpoint
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
      .then((response) => {
        if (response.data.ret === 0) {
          ElMessage.success('采购单完成');
          getPurchaseOrders();  // Reload purchase orders
        } else {
          ElMessage.error(response.data.msg);
        }
      })
      .catch((error) => {
        console.error('完成采购单失败:', error);
        ElMessage.error('完成采购单失败，请稍后重试！');
      });
  };
  
  // Call the function on component mount to load purchase orders
  onMounted(() => {
    getPurchaseOrders();
  });
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
  
  .purchase {
    padding: 20px;
    font-size: 18px;
    text-align: left;
    overflow-y: auto;
  }
  
  .purchase-list {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  
  .purchase-item {
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 5px;
    background-color: #f9f9f9;
    color: black;
  }
  
  hr {
    margin: 10px 0;
    border-top: 1px solid #ccc;
  }
  
  button {
    margin-top: 10px;
    padding: 10px 20px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #45a049;
  }
  </style>
  