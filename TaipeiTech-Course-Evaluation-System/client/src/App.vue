<template lang="pug">
  div
    navbar
    transition(name='el-fade-in-linear')
      router-view
    thefooter
</template>

<script>
import Navbar from '@/components/Navbar'
import Thefooter from '@/components/Thefooter'

export default {
  name: 'app',
  components: {
    Navbar,
    Thefooter
  }
}
</script>

<style>
@import url('//fonts.googleapis.com/css?family=Roboto');
@import url('//fonts.googleapis.com/earlyaccess/notosanstc.css');

body, html {
  margin: 0;
  height: 100%;
}

#app {
  font-family: 'Roboto', 'Noto Sans TC', "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微軟雅黑",Arial,sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}
</style>
