// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Vuex from 'vuex'
import { mapGetters, mapActions } from 'vuex'

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-default/index.css'
import store from '@/store'

import App from './App'
import router from './router'

Vue.use(Vuex)
Vue.use(ElementUI)

Vue.validators = {
  regex: (rule, value, callback) => {
    if (!rule.regex.test(value))
      return callback(new Error('Regex驗證格式錯誤'));
    callback();
  }
}

Vue.config.productionTip = false

router.beforeEach((to, from, next) => {
  console.log(to)
  if (to.path === '/login' ||
    to.path === '/register' ||
    to.path === '/authenticate' ||
    to.path === '/authenticate/confirm' ||
    to.path === '/about' ||
    to.path === '/'
  ) {
    next();
  } else {
    fetch(store.getters.api.status, {
      credentials: "include",
      method: 'GET'
    }).then(response => {
      return response.json();
    }).then(json => {
      if (json.result === -1) {
        store.getters.state.islogin = false;
        store.getters.state.islogin = false;
        next('/login');
      } else {
        store.getters.state.islogin = true;
        if (json.is_admin !== undefined && json.is_admin)
          store.getters.state.isadmin = true;
        if (json.result === -2)
          next('/authenticate');
        else
          next();
      }
    });
  }
});

/* eslint-disable no-new */
const app = new Vue({
  el: '#app',
  router,
  template: '<App/>',
  store,
  components: { App }
})
