<template lang="pug">
el-table(:data='data', v-loading="loading", element-loading-text='拚命加載中', row-dblclick='onClick')
    el-table-column(prop='name', label='課程名稱')
    el-table-column(prop='ccode', label='開課編號')
    el-table-column(prop='credits', label='學分')
    el-table-column(prop='hours', label='時數')
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'searchtable1',
  props: [
    'data',
    'loading'
  ],
  computed: {
  },
  methods: {
    onclick(row, column, cell, event) {
      console.log(row);
      console.log(column);
      console.log(cell);
      console.log(event);
    }
  }
}
</script>

<style lang="css" scoped>
</style>