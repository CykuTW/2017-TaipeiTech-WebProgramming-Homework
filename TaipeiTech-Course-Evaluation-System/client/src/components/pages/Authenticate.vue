<template lang="pug">
div
  el-row
    el-col(:span='20', :offset='2', style="text-align: center")
       p 您的帳號還沒有通過 E-Mail 認證唷，
       p 請盡快到信箱收取認證信完成認證。
       el-button(type='primary', @click='send()') 重寄認證信
</template>

<script>
import Vue from 'vue'
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'authenticate',
  components: {
  },
  computed: mapGetters([
    'api'
  ]),
  data() {
    return {
    }
  },
  methods: {
    send() {
      fetch(this.api.authenticate.send, {
        credentials: "include",
        method: 'POST',
      }).then((response) => {
        return response.json();
      }).then((json) => {
        if (json.result === 0) {
          this.$message.success({
            message: '重新寄送認證信成功'
          });
        } else {
          this.$message.error({
            message: '重新寄送認證信失敗'
          });
        }
        console.log(json);
      }).catch((error) => {
        console.log(error);
      });
    }
  }
}
</script>

<style lang="css" scoped>

</style>
