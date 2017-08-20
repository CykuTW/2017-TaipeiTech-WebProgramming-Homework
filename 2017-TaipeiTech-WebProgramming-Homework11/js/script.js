Vue.component('signin', {
    template: `
<div class="container">
    <div class="row" />
    <div class="row" />
    <div class="row">
        <div class="col s12">
            <div class="card">
                <div class="card-content">
                    <span class="card-title">Sign In</span>
                    <hr /><br /><br />
                    <div class="input-field">
                        <i class="material-icons prefix">email</i>
                        <input v-model="email" @keyup.enter="doSignin" placeholder="sample@gmail.com" id="email" type="email" class="validate">
                        <label for="email">E-Mail</label>
                    </div>
                    <div class="input-field">
                        <i class="material-icons prefix">input</i>
                        <input v-model="password" @keyup.enter="doSignin" id="password" type="password" class="validate">
                        <label for="password">Password</label>
                    </div>
                </div>
                <div class="center">
                    <button @click="doSignin" class="btn waves-effect waves-light">
                        SIGN IN
                        <i class="material-icons right">send</i>
                    </button>
                    <button @click="signup" class="btn waves-effect waves-light">
                        SIGN UP
                        <i class="material-icons right">account_circle</i>
                    </button>
                    <br /><br /><br />
                </div>
            </div>
        </div>
    </div>
</div>`,
    data: function() {
        return {
            email: '',
            password: ''
        }
    },
    methods: {
        doSignin: function () {
            //console.log(this.email);
            firebase.auth().signInWithEmailAndPassword(this.email, this.password).then(function(user) {
                if (user !== null) {
                    Materialize.toast('登入成功', 4000, 'green');
                    this.$root.page = 'info';
                }
            }).catch(function(error) {
                let errorCode = error.code;
                if (errorCode === 'auth/invalid-email') {
                    Materialize.toast('E-Mail 錯誤', 4000, 'red');
                } else if (errorCode === 'auth/user-not-found') {
                    Materialize.toast('不存在的使用者', 4000, 'red');
                } else if (errorCode === 'auth/wrong-password') {
                    Materialize.toast('密碼錯誤', 4000, 'red');
                }
            });
        },
        signup: function() {
            this.$root.page = 'signup';
        }
    },
    mounted: function() {
        //$('input').change(); //trigger all material input animation
    },
    beforeMount: function() {
        let user = firebase.auth().currentUser;
        if (user !== null) {
            this.$root.page = 'info';
        }
    },
});

var app = new Vue({
    el: '#app',
    template: `
<div>
    <navigation></navigation>
    <component :is="page"></component>
</div>
`,
    data: {
        page: 'signin'
    },
    mounted: function() {
        let root = this;
        firebase.auth().onAuthStateChanged(function(user) {
            if (user) {
                if (firebase.auth().currentUser !== null) {
                    root.page = 'info';
                } else {
                    root.page = 'signin';
                }
            }
        });
    }
});
Vue.config.devtools = false;
