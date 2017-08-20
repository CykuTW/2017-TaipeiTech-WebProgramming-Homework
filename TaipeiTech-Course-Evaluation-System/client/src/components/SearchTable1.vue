<template lang="pug">
el-table(:data='data', v-loading="loading", element-loading-text='拚命加載中', highlight-current-row, border=true, @row-dblclick='onClick')
    el-table-column(prop='cname', label='課程名稱', width='120', resizable=true, fixed='left')
    el-table-column(prop='code', label='開課編號')
    el-table-column(prop='credits', label='學分')
    el-table-column(prop='hours', label='時數')
    el-table-column(prop='cprog', label='標準')
    el-table-column(prop='class', label='班級')
    el-table-column(prop='tname', label='教師')
    el-table-column(prop='classroom', label='教室')
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
    onClick(row, event) {
      this.$router.replace({
        name: 'Course',
        params: {
          ccode: row.ccode
        }
      });
    }
  }
}
</script>

<style lang="css" scoped>
</style>