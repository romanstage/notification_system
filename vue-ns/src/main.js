import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify';
import 'roboto-fontface/css/roboto/roboto-fontface.css'
import '@fortawesome/fontawesome-free/css/all.css'
import axios from './plugins/api.service'
// import jwt_decode from 'jwt-decode'


Vue.config.productionTip = false;
Vue.prototype.$http = axios;
// Vue.prototype.$backendURL = 'http://172.21.128.50:8000'
Vue.prototype.$backendURL = 'http://127.0.0.1:8000/'
// const token = localStorage.getItem('access')
// if (token) {
//   Vue.prototype.$http.defaults.headers.common['Authorization'] = 'JWT ' + token
// }

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
