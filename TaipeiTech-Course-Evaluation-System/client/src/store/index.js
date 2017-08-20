import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)
// root state object.
// each Vuex instance is just a single state tree.
let prefix = 'http://localhost:5000'
const api = {
  prefix: prefix,
  status: prefix + '/status',
  logout: prefix + '/logout',
  login: prefix + '/login',
  register: prefix + '/register',
  course: {
    index: prefix + '/course',
    search1: prefix + '/course/search1',
    search2: prefix + '/course/search2'
  },
  evaluation: {
    index: prefix + '/evaluation',
    new: prefix + '/evaluation/new',
    total: prefix + '/evaluation/total'
  },
  report: prefix + '/report',
  admin: {
    evaluation: prefix + '/admin/evaluation',
    deletedEvaluation: prefix + '/admin/evaluation/deleted',
    report: prefix + '/admin/report',
    solvedReport: prefix + '/admin/report/solved'
  },
  authenticate: {
    confirm: prefix + '/authenticate/confirm',
    send: prefix + '/authenticate/send'
  }
}

const state = {
  show: false,
  islogin: false,
  isadmin: false
}

// mutations are operations that actually mutates the state.
// each mutation handler gets the entire state tree as the
// first argument, followed by additional payload arguments.
// mutations must be synchronous and can be recorded by plugins
// for debugging purposes.
const mutations = {
  toggleSidenav (state) {
    state.show = !state.show
  }
}

// actions are functions that causes side effects and can involve
// asynchronous operations.
const actions = {
  toggleSidenav: ({ commit }) => commit('toggleSidenav')
}

// getters are functions
const getters = {
  sideNavShowOrHide: state => {
    return state.show
  },
  state: () => {
    return state
  },
  api: () => {
    return api
  }
}

// A Vuex instance is created by combining the state, mutations, actions,
// and getters.
export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations
})