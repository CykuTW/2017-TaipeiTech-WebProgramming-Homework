Vue.component('navigation', {
    template: `
<nav class="teal" role="navigation">
    <div class="nav-wrapper container">
        <div class="brand-logo">Chatroom</div>
        <ul class="right hide-on-med-and-down black-text">
            <li><a @click="goto('info')">Information</a></li>
            <li><a @click="goto('chat')">Chat</a></li>
            <li><a @click="doSignout">Sign Out</a></li>
        </ul>
        <ul id="nav-mobile" class="side-nav">
            <li><a @click="goto('info')">Information</a></li>
            <li><a @click="goto('chat')">Chat</a></li>
            <li><a @click="doSignout"><i class="material-icons">exit_to_app</i>Sign Out</a></li>
        </ul>
        <a href="javascript:void(0)" data-activates="nav-mobile" class="button-collapse"><i class="material-icons">menu</i></a>
    </div>
</nav>
`,
    data: function() {
        return {
        }
    },
    methods: {
        goto: function(target) {
            this.$root.page = target;
            $('.button-collapse').sideNav('hide');
        },
        doSignout: function() {
            let component = this;
            let root = this.$root;
            if (firebase.auth().currentUser !== null) {
                firebase.auth().signOut().then(function() {
                    component.goto('signin');
                    Materialize.toast('登出成功', 4000, 'green');
                }, function(error) {
                    Materialize.toast('登出失敗', 4000, 'red');
                });
            }
        },
    },
    beforeMount: function() {
    },
    created: function(){
    },
    mounted: function() {
        $('.button-collapse').sideNav();
    }
});