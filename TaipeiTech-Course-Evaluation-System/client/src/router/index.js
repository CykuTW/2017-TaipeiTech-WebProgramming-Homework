import Vue from 'vue'
import { mapGetters, mapActions } from 'vuex'
import Router from 'vue-router'
import About from '@/components/pages/About'
import Login from '@/components/pages/Login'
import Course from '@/components/pages/Course'
import CourseSearch from '@/components/pages/CourseSearch'
import Evaluation from '@/components/pages/Evaluation'
import Register from '@/components/pages/Register'
import Authenticate from '@/components/pages/Authenticate'
import AuthenticateConfirm from '@/components/pages/AuthenticateConfirm'

import Admin from '@/components/pages/admin/Main'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: About
    },
    {
      path: '/about',
      name: 'about',
      component: About
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/course/search',
      name: 'CourseSearch',
      component: CourseSearch
    },
    {
      path: '/course/:ccode',
      name: 'Course',
      component: Course
    },
    {
      path: '/evaluation',
      name: 'Evaluation',
      component: Evaluation
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/admin',
      name: 'Admin',
      component: Admin
    },
    {
      path: '/authenticate/confirm',
      name: 'AuthenticateConfirm',
      component: AuthenticateConfirm
    },
    {
      path: '/authenticate',
      name: 'Authenticate',
      component: Authenticate
    }
  ]
})
