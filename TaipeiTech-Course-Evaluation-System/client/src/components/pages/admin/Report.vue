<template lang="pug">
div#evaluation(v-loading.fullscreen="fullscreenLoading")
  el-button(type='primary', @click='refreshData()') 重新整理
  template(v-for='report in reports')
    el-row
      el-col(:span='18', :offset='3')
        el-card(:body-style='{padding: "14px"}')
          div.clearfix(slot='header', style='text-align: center')
            span {{report.author.email}}:
            p(style='white-space: pre-line') {{report.reason}}
            div.bottom.clearfix
              el-button.button(type='success', @click='reportId = report.id; solvedReport()') 標記已解決
          el-rate(style="display: inline-block; margin-right: 4rem", v-model='report.evaluation.difficulty', disabled, show-text, text-color="#BB0909", text-template="困難度 {value}")
          el-rate(style="display: inline-block", v-model='report.evaluation.enrichment', disabled, show-text, text-color="#039E36", text-template="充實度 {value}")
          div(style='margin-top: 10px')
            el-tag(v-if='report.evaluation.deleted_at !== null', type='danger') 已刪除
            p(style='white-space: pre-line') {{report.evaluation.description}}
            div.bottom.clearfix
              time.time {{formatTime(report.post_time)}} # {{report.evaluation.id}}
              el-button.button(
                v-if='report.evaluation.deleted_at !== null',
                type='success', @click='evaluationId = report.evaluation.id; recoverEvaluation()'
              ) 還原
              el-button.button(
                v-if='report.evaluation.deleted_at === null',
                type='danger', @click='evaluationId = report.evaluation.id; deleteEvaluation()'
              ) 刪除
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
      reportId: 0,
      evaluationId: 0,
      currentPage: 1,
      totalPage: 0,
      reports: [
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
      fetch(this.api.admin.report + data, {
        credentials: "include",
        method: 'GET'
      }).then((response) => {
        return response.json();
      }).then((json) => {
        if (json.result !== 0) {
          throw Error();
        } else {
          this.reports = json.reports;
          this.totalPage = json.total;
        }
        this.fullscreenLoading = false;
      }).catch((error) => {
        console.log(error);
        this.fullscreenLoading = false;
      });
    },
    solvedReport() {
      this.$confirm('確定將此檢舉標記為已解決？', '提示', {
        confirmButtonText: '確定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        fetch(this.api.admin.report + '/' + this.reportId.toString(), {
          method: 'DELETE',
          credentials: "include",
        }).then((response) => {
          return response.json();
        }).then((json) => {
          if (json.result == 0) {
            this.$notify.success({
              title: '更改標記成功',
              message: ''
            });
          } else {
            this.$notify.error({
              title: '更改標記失敗',
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
    recoverEvaluation() {
      this.$confirm('確定還原此評價？', '提示', {
        confirmButtonText: '確定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        fetch(this.api.admin.evaluation + '/' + this.evaluationId.toString(), {
          method: 'PATCH',
          credentials: "include",
        }).then((response) => {
          return response.json();
        }).then((json) => {
          if (json.result == 0) {
            this.$notify.success({
              title: '還原成功',
              message: ''
            });
          } else {
            this.$notify.error({
              title: '還原失敗',
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
