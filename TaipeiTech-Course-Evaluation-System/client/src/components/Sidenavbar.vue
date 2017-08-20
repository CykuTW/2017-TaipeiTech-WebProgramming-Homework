<template lang="pug">
.sidenav-wrap
  el-col(:md='8', :sm='8').sidenav-container
    el-menu(theme='dark')
      el-menu-item(v-if='!state.islogin', index='/login', @click='toggleSidenav') 登入
      el-menu-item(v-if='state.islogin', index='/', @click='doLogout') 登出
      el-menu-item(v-if='state.isadmin', index='/admin', @click='toggleSidenav') 後台管理
      el-menu-item(index='/course/search', @click='toggleSidenav') 查詢課程
      el-menu-item(index='/evaluation', @click='toggleSidenav') 瀏覽評價
      el-menu-item(index='/about', @click='toggleSidenav') 關於 CES
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'sidenavbar',
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
      this.toggleSidenav();
    }
  }
}
</script>

<style lang="css" scoped>
.sidenav-container {
  position: fixed;
  top: 0;
  height: 100%;
  background-color: #324057;
  z-index: 999
}
@media screen and (max-width: 800px) {
  .el-menu-item {
    width: 100%
  }
}
</style>