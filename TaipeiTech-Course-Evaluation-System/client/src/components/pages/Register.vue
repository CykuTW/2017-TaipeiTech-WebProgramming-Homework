<template lang="pug">
div#register(v-loading.fullscreen='fullscreenLoading')
  el-row(:gutter='24')
    el-col(
      :xs='{span: 20, offset: 2}'
      :sm='{span: 14, offset: 5}'
      :md='{span: 10, offset: 7}'
      :lg='{span: 8, offset: 8}'
    )
      h2 註冊 TaipeiTech CES
      el-card.box-card
        el-form#loginForm(ref='loginForm', :model='loginForm', :rules='loginRules', label-position="right", label-width="80px")
          el-form-item(label='E-Mail', prop='email')
            el-input(name='email', placeholder='example@ntut.edu.tw', v-model='loginForm.email', type='email', auto-complete='off')
          el-form-item(label='密碼', prop='password')
            el-input(name='password', v-model='loginForm.password', type='password', auto-complete='off')
          el-form-item
            el-button(type='primary', @click="submitForm('loginForm')") 註冊
            el-button(@click="resetForm('loginForm')") 清除
</template>

<script>
import Vue from 'vue'
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'login',
  components: {
  },
  computed: mapGetters([
    'api'
  ]),
  data() {
    return {
      fullscreenLoading: false,
      loginForm: {
        email: '',
        password: ''
      },
      loginRules: {
        email: [
          { required: true, message: 'E-Mail不得為空', trigger: 'blur' },
          { regex: /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@ntut.edu.tw$/,
            message: 'E-Mail格式錯誤',
            type: 'email',
            validator: Vue.validators.regex,
            trigger: 'blur'
          }
        ],
        password: [
          { required: true, message: '密碼不得為空', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.fullscreenLoading = true;
          fetch(this.api.register, {
            credentials: "include",
            method: 'POST',
            headers: {
              'Content-Type':'application/x-www-form-urlencoded'
            },
            body: $('#loginForm').serialize()
          }).then((response) => {
            return response.json();
          }).then((json) => {
            if (json.result === -1) {
              this.$notify.error({
                title: '註冊失敗',
                message: '參數錯誤'
              });
            } if (json.result === -2) {
              this.$notify.error({
                title: '註冊失敗',
                message: '使用者已存在'
              });
            } else if (json.result === 0) {
              this.$notify.success({
                title: '註冊成功',
                message: '請至 E-Mail 信箱收取認證信後再登入'
              });
            }
            this.fullscreenLoading = false;
          }).catch((error) => {
            console.log(error);
            this.fullscreenLoading = false;
          });
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    }
  }
}
</script>

<style lang="css" scoped>
#register {
  margin-top: 3rem;
}
</style>
