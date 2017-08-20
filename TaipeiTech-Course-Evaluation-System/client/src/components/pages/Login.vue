<template lang="pug">
div#login
  el-row(:gutter='24')
    el-col(
      :xs='{span: 20, offset: 2}'
      :sm='{span: 14, offset: 5}'
      :md='{span: 10, offset: 7}'
      :lg='{span: 8, offset: 8}'
    )
      h2 登入 TaipeiTech CES
      el-card.box-card
        el-form#loginForm(ref='loginForm', :model='loginForm', :rules='loginRules', label-position="right", label-width="80px")
          el-form-item(label='E-Mail', prop='email')
            el-input(name='email', placeholder='example@ntut.edu.tw', v-model='loginForm.email', type='email', auto-complete='off')
          el-form-item(label='密碼', prop='password')
            el-input(name='password', v-model='loginForm.password', type='password', auto-complete='off')
          el-form-item
            el-button(type='primary', @click="submitForm('loginForm')") 登入
            el-button(@click="resetForm('loginForm')") 清除
            el-button(@click="$router.replace({name: 'Register',})") 註冊
</template>

<script>
import Vue from 'vue'
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'register',
  components: {
  },
  computed: mapGetters([
    'api', 'state'
  ]),
  data() {
    return {
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
          fetch(this.api.login, {
            credentials: "include",
            method: 'POST',
            headers: {
              'Content-Type':'application/x-www-form-urlencoded'
            },
            body: $('#loginForm').serialize()
          }).then((response) => {
            return response.json();
          }).then((json) => {
            if (json.result === 0) {
              this.state.islogin = true;
              this.$notify.success({
                title: '登入成功',
                message: ''
              });
              this.$router.replace({name: 'CourseSearch'});
            } else if (json.result === -1) {
              this.state.islogin = false;
              this.$notify.error({
                title: '登入失敗',
                message: '參數錯誤'
              });
            } else if (json.result === -2) {
              this.state.islogin = false;
              this.$notify.error({
                title: '登入失敗',
                message: 'E-Mail或密碼輸入錯誤'
              });
            }
            console.log(json);
          }).catch((error) => {
            console.log(error);
          });
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    resetForm(formName) {
      /* fetch(this.api.status, {
        method: 'GET',
        credentials: "include"
      }).then((response) => {
        return response.json();
      }).then((json) => {
        console.log(json);
      }).catch((error) => {
        console.log(error);
      }) */
      this.$refs[formName].resetFields();
    }
  }
}
</script>

<style lang="css" scoped>
#login {
  margin-top: 3rem;
}
</style>
