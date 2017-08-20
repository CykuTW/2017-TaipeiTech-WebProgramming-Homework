<template lang="pug">
div#course
  el-row
    el-col(:span='22', :offset='1')
      el-card.box-card
        el-form(label-position="right", label-width="90px")
          el-row
            el-col(
              :xs='{span: 24, offset: 0}'
              :sm='{span: 8, offset: 0}'
              :md='{span: 6, offset: 0}'
              :lg='{span: 6, offset: 0}'
            )
              el-form-item(label='課程編碼\n\nCode')
                el-input(v-model='course.ccode', readonly)
            el-col(
              :xs='{span: 24, offset: 0}'
              :sm='{span: 16, offset: 0}'
              :md='{span: 18, offset: 0}'
              :lg='{span: 18, offset: 0}'
            )
              el-form-item(label='課程名稱\n\nName')
                el-input(v-model='course.name', type="textarea", :rows='3', readonly)
          el-form-item(label='中文概述\n\nChinese Description')
            el-input(v-model='course.chinese_description', type="textarea", :rows='5', readonly)
          el-form-item(label='英文概述\n\nEnglish Description')
            el-input(v-model='course.english_description', type="textarea", :rows='5', readonly)
  el-row(v-loading.body='loading')
    el-dialog(title='發表新的評價', :visible.sync="dialogFormVisible")
      el-form(label-position="right", label-width="90px")
        el-form-item(label='課程編碼\n\nCode')
          el-input(v-model='course.ccode', type="textarea", readonly)
        el-form-item(label='課程名稱\n\nName')
          el-input(v-model='course.name', type="textarea", :rows='2', readonly)
        el-form-item(label='心得')
          el-input(v-model='experience', type='textarea', :rows='8')
        div.block
          span.demonstration(style='color: #BB0909') 困難度
          el-slider(v-model='difficulty', :step='0.1', :max='5', show-input)
        div.block
          span.demonstration(style='color: #039E36') 充實度
          el-slider(v-model='enrichment', :step='0.1', :max='5', show-input)
      div.dialog-footer(slot='footer')
        el-button(@click='dialogFormVisible = false') 取消
        el-button(type='primary', @click='submitEvaluation()') 送出
    el-row
      el-col(:span='22', :offset='1')
        el-form
          el-form-item
            el-button(type='primary', icon='edit', @click='dialogFormVisible = true') 發表評價
        template(v-for='(evaluation, index) in evaluations')
          el-row(v-if='index % 2 === 0')
            el-col(
              :xs='{span: 24, offset: 0}',
              :sm='{span: 11, offset: 0}',
              :md='{span: 11, offset: 0}',
              :lg='{span: 11, offset: 0}',
              style='margin-bottom: 1.5rem'
            )
              el-card(:body-style='{padding: "14px"}')
                el-rate(v-model='evaluation.difficulty', disabled, show-text, text-color="#BB0909", text-template="困難度 {value}")
                el-rate(v-model='evaluation.enrichment', disabled, show-text, text-color="#039E36", text-template="充實度 {value}")
                div(style='margin-top: 10px')
                  span {{evaluation.description}}
                  div.bottom.clearfix
                    time.time {{formatTime(evaluation.post_time)}} # {{evaluation.id}}
                    el-button.button(type='danger', @click='reportId = evaluation.id; dialogReportVisible = true') 檢舉此評價
            el-col(
              :xs='{span: 24, offset: 0}',
              :sm='{span: 11, offset: 2}',
              :md='{span: 11, offset: 2}',
              :lg='{span: 11, offset: 2}',
              v-if='evaluations[index+1] !== undefined',
              style='margin-bottom: 1.5rem'
            )
              el-card(:body-style='{padding: "14px"}')
                el-rate(v-model='evaluations[index+1].difficulty', disabled, show-text, text-color="#BB0909", text-template="困難度 {value}")
                el-rate(v-model='evaluations[index+1].enrichment', disabled, show-text, text-color="#039E36", text-template="充實度 {value}")
                div(style='margin-top: 10px')
                  span {{evaluations[index+1].description}}
                  div.bottom.clearfix
                    time.time {{formatTime(evaluations[index+1].post_time)}} # {{evaluations[index+1].id}}
                    el-button.button(type='danger', @click='reportId = evaluations[index+1].id; dialogReportVisible = true') 檢舉此評價
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
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'course',
  props: [
  ],
  computed: mapGetters([
    'api'
  ]),
  methods: {
  },
  data() {
    return {
      dialogReportVisible: false,
      reportId: 1,
      reason: '',
      loading: false,
      difficulty: 0,
      enrichment: 0,
      experience: '',
      dialogFormVisible: false,
      course: {
        ccode: '',
        name: '',
        credits: '',
        hours: '',
        chinese_description: '',
        english_description: ''
      },
      evaluations: [

      ]
    }
  },
  methods: {
    submitEvaluation() {
      if (this.difficulty < 0 || this.difficulty > 5) {
        this.$notify.error({
          title: '錯誤',
          message: '困難度只能為介於0~5的數字'
        });
        return;
      }
      if (this.enrichment < 0 || this.enrichment > 5) {
        this.$notify.error({
          title: '錯誤',
          message: '充實度只能為介於0~5的數字'
        });
        return;
      }
      if (this.experience.trim() === '') {
        this.$notify.error({
          title: '錯誤',
          message: '心得不能為空白'
        });
        return;
      }

      let data = '';
      data += '&ccode=' + encodeURIComponent(this.course.ccode);
      data += '&experience=' + encodeURIComponent(this.experience);
      data += '&difficulty=' + encodeURIComponent(this.difficulty.toString());
      data += '&enrichment=' + encodeURIComponent(this.enrichment.toString());
      fetch(this.api.evaluation.new, {
        credentials: "include",
        method: 'POST',
        headers: {
          'Content-Type':'application/x-www-form-urlencoded'
        },
        body: data
      }).then((response) => {
        return response.json();
      }).then((json) => {
        if (json.result !== 0) {
          throw Error();
        } else {
          this.refreshData();
          this.dialogFormVisible = false;
          this.experience = '';
          this.experience = 0;
          this.enrichment = 0;
          this.$notify.success({
            title: '新增成功',
            message: '請靜待資料庫更新',
          });
        }
      }).catch((error) => {
        this.$notify.error({
          title: '失敗',
          message: '新增評價失敗，請稍後再試'
        });
        console.log(error);
      });
    },
    refreshData() {
      let url = this.api.course.index + '/' + this.$route.params.ccode;
      fetch(url, {
        method: 'GET',
        credentials: "include"
      }).then((response) => {
        return response.json();
      }).then((json) => {
        if (json.result == 0) {
          this.course = json.course;
          this.refreshEvaluations();
        }
      }).catch((error) => {
        console.log(error);
      })
    },
    refreshEvaluations() {
      this.loading = true;
      let url = this.api.evaluation.index + '/' + this.$route.params.ccode;
      fetch(url, {
        method: 'GET',
        credentials: "include"
      }).then((response) => {
        return response.json();
      }).then((json) => {
        if (json.result == 0) {
          this.evaluations = json.evaluations;
        }
        this.loading = false;
      }).catch((error) => {
        console.log(error);
        this.loading = false;
      })
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
  }
}
</script>

<style lang="css">
#course > .el-row {
  margin-top: 1.5rem;
}

.el-form-item__label {
  white-space: pre-line !important;
}

.button {
  padding: 5px;
  float: right;
}

.time {
  line-height: 28px;
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