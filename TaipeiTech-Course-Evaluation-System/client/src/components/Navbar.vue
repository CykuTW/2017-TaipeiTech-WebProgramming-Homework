<template lang="pug">
div
  el-menu.navbar(theme='dark', mode='horizontal', :router='true')
    .logo-container
      img.logo-img(src="../assets/TaipeiTech.png")
    #toggle-sidenav-btn(index='#', @click='toggleSidenav') ☰
    .navbar-items-wrap
      el-menu-item(v-if='!state.islogin', index='/login') 登入
      el-menu-item(v-if='state.islogin', index='/', @click='doLogout') 登出
      el-menu-item(v-if='state.isadmin', index='/admin') 後台管理
      el-menu-item(index='/course/search') 查詢課程
      el-menu-item(index='/evaluation') 瀏覽評價
      el-menu-item(index='/about') 關於 CES
  transition(name='el-zoom-in-top')
    sidenavbar(v-show='sideNavShowOrHide')
  .sidenav-mask(v-show='sideNavShowOrHide', @click='toggleSidenav')
</template>

<script>
import Sidenavbar from '@/components/Sidenavbar'
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'navbar',
  data() {
    return {
    }
  },
  components: {
    Sidenavbar
  },
  computed: mapGetters([
    'sideNavShowOrHide',
    'api', 'state'
  ]),
  methods: {
    ...mapActions([
      'toggleSidenav'
    ]),
    doLogout() {
      fetch(this.api.logout, {
        credentials: "include",
        method: 'GET'
      }).then((response) => {
        this.state.islogin = false;
        this.state.isadmin = false;
        this.$router.replace({name: 'Home'});
      }).catch((error) => {
        console.log(error);
      });
    }
  }
}
</script>

<style lang="css">
.navbar {
  background-color: #1D8CE0;
}
#toggle-sidenav-btn {
  display: none;
}
.el-menu-item {
  color: #fff !important;
}
.el-menu-item.is-active {
  color: #ee0 !important;
}
.logo-container {
  margin-top: .1rem;
  margin-left: 3rem;
  margin-right: 2rem;
  background-color: #fff;
  padding: 0 1rem;
  border-radius: 500px;
  width: 124.39px;
  height: 55px;
  float: left;
  cursor: default;
}
.logo-img {
  float: left;
  height: 55px;
}
.logo-container {
  float: left
}
.sidenav-mask {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #111;
  opacity: .5;
  z-index: 998
}
@media screen and (max-width: 800px) {
  .navbar-items-wrap {
    display: none;
  }
  #toggle-sidenav-btn {
    position: absolute;
    top: 1.5rem;
    left: 2rem;
    display: inline-block;
    color: #fff
  }
  .logo-container {
    float: none;
    margin: .5rem auto
  }
  .el-menu-item {
    float: none !important;
    display: inline-block;
    color: #123
  }
}
@media screen and (max-width: 480px) {
  #toggle-sidenav-btn {
    left: 1.2rem;
  }
  .logo-container {
    width: 150px;
    padding: 0 1rem
  }
}
</style>
