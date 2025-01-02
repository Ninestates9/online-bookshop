import { defineStore } from 'pinia';
import { ref, onMounted } from 'vue';

// 定义 Store
export const mainStore = defineStore('main', {
  state: () => ({
    userid:localStorage.getItem('userid') || '',
    username:'username',
    address:'翻斗大街 翻斗花园 二号楼1001室',
    password:'password',
    balance:100000,
    usermessage:'嘻嘻',
    searchOP:null,
    ip:'http://10.19.129.45:5000',
    userlevel:5,
    total:0,
    cartItems: ref([]),
    overdraft:0,
  }),
  getters: {},
  actions: {
    setUserId(id: string) {
      this.userid = id;
      localStorage.setItem('userid', id); // 将 userid 保存到 LocalStorage
    },
    clearUserId() {
      this.userid = '';
      localStorage.removeItem('userid'); // 清除 LocalStorage 中的值
    },
    addToCart(item) {
      // 确保 cartItems 是有效的数组并且可以正常调用 push
      if (Array.isArray(this.cartItems)) {
        this.cartItems.push(item);
      } else {
        console.error('cartItems is not an array');
        this.cartItems = [];  // 如果不是数组，则重新初始化
        this.cartItems.push(item);
      }
    },
    
  },
});

