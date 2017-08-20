<template lang="pug">
div
  el-row
    el-col(:span='20', :offset='2')
      h2 關於 TaipeiTech CES
</template>

<script>
import Vue from 'vue'
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'about',
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
  }
}
</script>

<style lang="css" scoped>

</style>
