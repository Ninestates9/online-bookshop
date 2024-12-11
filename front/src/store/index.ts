import { defineStore } from 'pinia';

// 定义 Store
export const mainStore = defineStore('main', {
  state: () => ({
    ipAddress: 'http://123.57.215.19:5000',
    isShow: false,
    showMindMap: false,
    editorisShow: false,
    openStyleID: null,
    openNoteID: null,
    usedStyleID: null,
    htmlContent: null,
    editor: null,
    username: null,
    content: null,
    select: null,
    isLoading: false,
    isOpen: false,
    headings: [],
    background: "night_background",
    theme: localStorage.getItem('theme') || 'dark',
  }),
  getters: {},
  actions: {
    
  },
});

