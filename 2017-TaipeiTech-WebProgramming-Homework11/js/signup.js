Vue.component('signup', {
    template: `
<div class="container">
    <div class="row" />
    <div class="row" />
    <div class="row">
        <div class="col s12">
            <div class="card">
                <div class="card-content">
	            <span class="card-title"><i class="material-icons prefix">add_circle_outline</i>Sign Up New User</span>	
                    <hr />
	            <h5 class="teal-text">Join us! Let's chat!</h5>
                    <br /><br />
                    <div class="input-field">
                        <i class="material-icons prefix">email</i>
                        <input v-model="email" placeholder="sample@gmail.com" id="email" type="email" class="validate">
                        <label for="email">E-Mail</label>
                    </div>
                    <div class="input-field">
                        <i class="material-icons prefix">input</i>
                        <input v-model="password" id="password" type="password" class="validate">
                        <label for="password">Password</label>
                    </div>
                </div>
                <div class="center">
                    <a href="#confirm" class="btn waves-effect waves-light">
                        SIGN UP
                        <i class="material-icons right">send</i>
                    </a>
                    <button @click="back" class="btn waves-effect waves-light">
                        BACK
                        <i class="material-icons right">exit_to_app</i>
                    </button>
                    <div id="confirm" class="modal">
                        <div class="modal-content">
                            <h4>Confirm</h4>
                            <p>Are you sure that you wanna sign up with {{email}}</p>
                        </div>
                        <div class="modal-footer">
                            <a class="modal-action modal-close waves-effect waves-green btn-flat">Disagree</a>
                            <a @click="doSignup" class="modal-action modal-close waves-effect waves-green btn-flat">Agree</a>
                        </div>
                    </div>
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
        doSignup: function () {
            //console.log(this.email);
            firebase.auth().createUserWithEmailAndPassword(this.email, this.password).then(function(user){
                Materialize.toast('註冊成功', 4000, 'green');
                firebase.database().ref('/users/' + user.uid).set({
                    username: '',
                    occupation: '',
                    age: 0,
                    description: '',
                    email: ''
                });
                this.$root.page = 'signin';
            }).catch(function(error) {
                let errorCode = error.code;
                if (errorCode === 'auth/email-already-in-use') {
                    Materialize.toast('失敗，E-Mail 已被使用', 4000, 'red');
                } else if (errorCode === 'auth/invalid-email') {
                    Materialize.toast('失敗，不合法的 E-Mail', 4000, 'red');
                } else if (errorCode === 'auth/weak-password') {
                    Materialize.toast('失敗，密碼太弱，至少需超過 6 個字元', 4000, 'red');
                }
            });

            let user = firebase.auth().currentUser;
            if (user !== null) {
                /*firebase.database().ref('/users/' + user.uid).set({
                    email: user.email
                }).catch(function(error) {
                    console.error("寫入使用者資訊錯誤",error);
                });*/
                this.$root.page = 'updateInfo';
            }
        },
        back: function() {
            this.$root.page = 'signin';
        }
    },
    mounted: function() {
        $('input').change(); //trigger all material input animation
        $('.modal').modal();
    },
    beforeMount: function() {
        let user = firebase.auth().currentUser;
        if (user !== null) {
            this.$root.page = 'info';
        }
    },
});
