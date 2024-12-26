import { defineStore } from 'pinia';

// 定义 Store
export const mainStore = defineStore('main', {
  state: () => ({
    userid:'userid',
    username:'username',
    address:'翻斗大街 翻斗花园 二号楼1001室',
    password:'password',
    balance:100000,
    usermessage:'嘻嘻',
    searchOP:'',
    ip:'http://10.16.203.225:5000',
    userlevel:5,
    total:0,
  }),
  getters: {},
  actions: {
    
  },
});

