import Vue from 'vue';
import Router from 'vue-router';
import Home from '@/components/Home.vue';
import ChatWindow from '@/components/ChatWindow.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/chats',
      name: 'ChatWindow',
      component: ChatWindow
    }
  ]
});
