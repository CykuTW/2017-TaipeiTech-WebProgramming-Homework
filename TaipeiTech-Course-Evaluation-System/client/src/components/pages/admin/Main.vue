<template lang="pug">
div#admin
  el-row
    el-col(:span='22', :offset='1')
      el-tabs(v-model='activeName', type='border-card')
        el-tab-pane(label='評價列表', name='first')
          evaluation
        el-tab-pane(label='檢舉列表', name='second')
          report
        el-tab-pane(label='評價垃圾桶', name='third')
          deleted-evaluation
        el-tab-pane(label='已處理檢舉', name='fourth')
          solved-report
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import Evaluation from '@/components/pages/admin/Evaluation'
import DeletedEvaluation from '@/components/pages/admin/DeletedEvaluation'
import Report from '@/components/pages/admin/Report'
import SolvedReport from '@/components/pages/admin/SolvedReport'


export default {
  name: 'admin',
  data() {
    return {
      activeName: 'first'
    }
  },
  components: {
    Evaluation,
    DeletedEvaluation,
    Report,
    SolvedReport
  },
  computed: mapGetters([
    'api', 'state'
  ]),
  methods: {
  }
}
</script>

<style lang="css" scoped>
#admin {
  margin-top: 3rem;
}
</style>
