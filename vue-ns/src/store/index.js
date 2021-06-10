import Vue from 'vue'
import Vuex from 'vuex'
import TextareaAutosize from 'vue-textarea-autosize'

import { auth } from './auth.module';
import { alerts } from './alerts.module'
import { dialog } from "./confirmDialog.module";

import { contactDetailModal } from './contactDetailModal.module'
import { groupDeleteModal } from './groupDeleteModal.module'
import { genericModal } from './genericModal.module'
import { createContactModal } from './createContactModal.module'

Vue.use(Vuex)
Vue.use(TextareaAutosize)
const store = new Vuex.Store({
  state: {
        // backendUrl: 'http://172.21.128.50:8000',
        // validToken: ''
  },
  mutations: {

  },
  actions: {

  },
  modules: {
    auth,
    alerts,
    dialog,
    contactDetailModal,
    groupDeleteModal,
    genericModal,
    createContactModal,
  },
  getters: {
    // getServerUrl: state => {
    //   return state.backendUrl
    // },
    // getToken: state => {
    //   return state.validToken
    // },
    getAuthState: state => {
      return state.auth.status.loggedIn
    },
    getHaveGroup: state => {
      return state.auth.status.haveGroup
    },
  }
})


store.dispatch('auth/refresh');

export default store


