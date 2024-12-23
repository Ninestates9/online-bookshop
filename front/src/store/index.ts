import { defineStore } from 'pinia';

// 定义 Store
export const mainStore = defineStore('main', {
  state: () => ({
    userid:'userid',
    username:'username',
    address:'翻斗大街 翻斗花园 二号楼1001室',
    balance:100000,
    usermessage:'嘻嘻'
  }),
  getters: {},
  actions: {
    
  },
});

