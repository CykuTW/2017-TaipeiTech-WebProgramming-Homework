<template lang="pug">
div#evaluation(v-loading.fullscreen="fullscreenLoading")
  el-button(type='primary', @click='refreshData()') 重新整理
  template(v-for='evaluation in evaluations')
    el-row
      el-col(:span='18', :offset='3')
        el-card(:body-style='{padding: "14px"}')
          div.clearfix(slot='header', style='text-align: center')
            p(style='white-space: pre-line') {{evaluation.course.ccode}} {{evaluation.course.name}}
          el-rate(style="display: inline-block; margin-right: 4rem", v-model='evaluation.difficulty', disabled, show-text, text-color="#BB0909", text-template="困難度 {value}")
          el-rate(style="display: inline-block", v-model='evaluation.enrichment', disabled, show-text, text-color="#039E36", text-template="充實度 {value}")
          div(style='margin-top: 10px')
            p(style='white-space: pre-line') {{evaluation.description}}
            div.bottom.clearfix
              time.time {{formatTime(evaluation.post_time)}} # {{evaluation.id}}
              el-button.button(type='danger', @click='evaluationId = evaluation.id; deleteEvaluation()') 刪除
  el-row
    el-col(:span='18', :offset='3')
      div(style='text-align: center')
        el-pagination(
          style='display: inline-block',
          @current-change="handleCurrentChange",
          :current-page="currentPage",
          layout="total, prev, pager, next, jumper",
          :total="totalPage"
        )
</template>

<script>
import Vue from 'vue'
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'evaluation',
  components: {
  },
  computed: mapGetters([
    'api'
  ]),
  data() {
    return {
      evaluationId: 0,
      currentPage: 1,
      totalPage: 0,
      evaluations: [
      ],
      fullscreenLoading: false
    }
  },
  methods: {
    handleCurrentChange(val) {
      this.currentPage = val;
      this.refreshData();
    },
    refreshData() {
      this.fullscreenLoading = true;

      let data = '?';
      data += '&page=' + encodeURIComponent(this.currentPage.toString());
      fetch(this.api.evaluation.index + data, {
        credentials: "include",
        method: 'GET'
      }).then((response) => {
        return response.json();
      }).then((json) => {
        if (json.result !== 0) {
          throw Error();
        } else {
          this.evaluations = json.evaluations;
          this.totalPage = json.total;
        }
        this.fullscreenLoading = false;
      }).catch((error) => {
        console.log(error);
        this.fullscreenLoading = false;
      });
    },
    deleteEvaluation() {
      this.$confirm('確定刪除此評價？', '提示', {
        confirmButtonText: '確定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        fetch(this.api.admin.evaluation + '/' + this.evaluationId.toString(), {
          method: 'DELETE',
          credentials: "include",
        }).then((response) => {
          return response.json();
        }).then((json) => {
          if (json.result == 0) {
            this.$notify.success({
              title: '刪除成功',
              message: ''
            });
          } else {
            this.$notify.error({
              title: '刪除失敗',
              message: ''
            });
          }
          this.refreshData();
        }).catch((error) => {
          console.log(error);
        })
      }).catch(() => {
      });
    },
    formatTime(timestamp) {
      let d = new Date(timestamp);
      let result = '';
      result += d.getFullYear() + '-';
      result += d.getMonth() + '-';
      result += d.getDate() + ' ';
      result += ('00'+d.getHours().toString()).slice(-2) + ':';
      result += ('00'+d.getMinutes().toString()).slice(-2) + ':';
      result += ('00'+d.getSeconds().toString()).slice(-2);
      return result;
    }
  },
  mounted() {
    this.refreshData();
  }
}
</script>

<style lang="css">
#evaluation > .el-row {
  margin-top: 1.5rem;
}

.button {
  padding: 5px;
  float: right;
}

.time {
  font-size: 13px;
  color: #999;
}

.bottom {
  margin-top: 13px;
  line-height: 12px;
}

.clearfix:before,
.clearfix:after {
    display: table;
    content: "";
}

.clearfix:after {
    clear: both
}
</style>
