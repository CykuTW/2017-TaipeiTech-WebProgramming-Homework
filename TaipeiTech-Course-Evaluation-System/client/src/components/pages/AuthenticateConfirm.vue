<template lang="pug">
div(v-loading.fullscreen='loading')
</template>

<script>
import Vue from 'vue'
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'authenticateConfirm',
  components: {
  },
  computed: mapGetters([
    'api'
  ]),
  data() {
    return {
      loading: true
    }
  },
  methods: {
    send() {
      
    }
  },
  mounted() {
    console.log('test');
    let data = '';
    data += '&token=' + encodeURIComponent(this.$route.query.t);
    data += '&id=' + encodeURIComponent(this.$route.query.id);
    fetch(this.api.authenticate.confirm, {
      credentials: "include",
      method: 'POST',
      headers: {
        'Content-Type':'application/x-www-form-urlencoded'
      },
      body: data
    }).then((response) => {
      return response.json();
    }).then((json) => {
      this.loading = false;
      if (json.result === 0) {
        this.$message.success({
          message: 'E-Mail 認證成功',
          duration: 0
        });
      } else {
        this.$message.error({
          message: 'E-Mail 認證失敗',
          duration: 0
        });
      }
      console.log(json);
    }).catch((error) => {
      console.log(error);
    });
  }
}
</script>

<style lang="css" scoped>

</style>
