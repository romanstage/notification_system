import Vue from 'vue'
import VueRouter from 'vue-router'
import HomePage from '@/views/HomePage'
import Auth from '@/views/Auth'
import Contacts from '@/views/Contacts'
import AccessDenied from '@/views/AccessDenied'
import ServerError from '@/views/ServerError'
import NoGroup from '@/views/NoGroup'
import store from '../store/index'
import GroupList from '@/components/Group/GroupList'
import GroupEdit from '@/views/GroupEdit'
import TemplateList from '@/components/Templates/TemplateList'

Vue.use(VueRouter)

const publicPages = ['/login', '/register', '/home', '/access-denied', '/server-error', '/no-group',];

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
  {
      path: '/login',
      name: 'Auth',
      component: Auth
  },
  {
      path: '/contacts',
      name: 'Contacts',
      component: Contacts
  },

  {
      path: '/groups',
      name: 'Groups',
      component: GroupList
  },
      {
      path: '/group-edit/:group_id',
      name: 'GroupEdit',
      component: GroupEdit
  },



  {
      path: '/access-denied',
      name: 'AccessDenied',
      component: AccessDenied
  },
  {
      path: '/no-group',
      name: 'NoGroup',
      component: NoGroup
  },

    {
      path: '/server-error',
      name: 'ServerError',
      component: ServerError
  },

    {
      path: '/templates',
      name: 'Templates',
      component: TemplateList
  }




]

const router = new VueRouter({
  mode: 'history',
  routes
})


export default router

router.beforeEach((to, from, next) => {
  const authRequired = !publicPages.includes(to.path);
 if (authRequired && !store.getters.getAuthState) {
        next('/login');
    }
 else {
     next();
 }
});

router.beforeEach((to, from, next) => {
    const authRequired = !publicPages.includes(to.path);
    if (authRequired && !store.getters.getHaveGroup && store.getters.getAuthState) {
      next('/no-group');
    }
    else {
        next();
    }
});

