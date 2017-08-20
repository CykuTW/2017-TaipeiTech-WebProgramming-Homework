<template lang="pug">
div#evaluation(v-loading.fullscreen="fullscreenLoading")
  el-row
    el-col(:span='18', :offset='3', style='text-align: center')
      h2 最新評價
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
              el-button.button(type='danger', @click='reportId = evaluation.id; dialogReportVisible = true') 檢舉此評價
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
  el-dialog(:title='"檢舉評價 #" + reportId.toString()', :visible.sync='dialogReportVisible')
    el-form(label-position='right', label-width='40px')
      el-form-item(label='理由')
        el-input(v-model='reason', type='textarea', :rows='8')
    div.dialog-footer(slot='footer')
      el-button(@click='dialogReportVisible = false') 取消
      el-button(type='danger' @click='reportEvaluation()') 送出
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
      reason: '',
      dialogReportVisible: false,
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
    reportEvaluation() {
      if (this.reason.trim() === '') {
        this.$notify.error({
          title: '錯誤',
          message: '理由不能為空'
        });
        return;
      }

      this.$confirm('按下確定將送出檢舉，請確認內容是否無誤？', '提示', {
        confirmButtonText: '確定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        let data = '';
        data += '&id=' + encodeURIComponent(this.reportId.toString());
        data += '&reason=' + encodeURIComponent(this.reason);
        fetch(this.api.report, {
          method: 'POST',
          headers: {
            'Content-Type':'application/x-www-form-urlencoded'
          },
          credentials: "include",
          body: data
        }).then((response) => {
          return response.json();
        }).then((json) => {
          if (json.result == 0) {
            this.$notify.success({
              title: '檢舉成功',
              message: '請等待管理員進行審核'
            });
          } else {
            this.$notify.error({
              title: '錯誤',
              message: '檢舉失敗'
            });
          }
          this.reason = '';
          this.dialogReportVisible = false;
        }).catch((error) => {
          console.log(error);
          this.reason = '';
          this.dialogReportVisible = false;
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
    this.fullscreenLoading = true;
    let that = this;
    fetch(this.api.evaluation.total, {
        credentials: "include",
        method: 'GET'
    }).then((response) => {
        return response.json();
    }).then((json) => {
      if (json.result !== 0) {
        throw Error();
      } else {
        that.totalPage = json.total;
        that.fullscreenLoading = false;
      }
    }).catch((error) => {
      console.log(error);
      that.fullscreenLoading = false;
    });
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
