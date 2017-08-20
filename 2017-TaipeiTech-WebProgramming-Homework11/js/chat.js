Vue.component('message-box', {
    template: `
<li class="collection-item avatar">
    <img style="width: 50px; height: 50px;" class="circle" :src="sticker" />
    <!-- <i class="material-icons circle red">play_arrow</i> -->
    <span class="title blue-text">{{username}}</span>
    <p style="word-wrap: break-word">{{message}}</p>
</li>
`,
    props: [
        'user',
        'message'
    ],
    data: function() {
        return {
            username: 'No-Name',
            sticker: ''
        }
    },
    methods: {

    },
    created: function() {
        let component = this;
        firebase.database().ref('/users/' + this.user).once('value').then(function (snapshot) {
            component.username = snapshot.val().username;
            if (component.username === '') {
                component.username = 'No-Name';
            }
        });
        firebase.storage().ref('/sticker/' + this.user).getDownloadURL().then(function(url) {
            component.sticker = url;
        }).catch(function(error){
            firebase.storage().ref('/sticker/defaultSticker').getDownloadURL().then(function(url) {
                component.sticker = url;
            }).catch(function(error){});
        });
    }
});

Vue.component('chat', {
    template: `
<div class="container">
<div class="row" style="margin: 0">
<div class="col s12" >
    <ul id="message-list" class="collection" style="overflow-y: scroll; height: 75vh; margin-bottom: 0">
        <message-box
            v-for="message in messageList"
            v-bind:key="message.id"
            v-bind:user="message.user"
            v-bind:message="message.message"
            v-bind:postTime="message.postTime">
        </message-box>
     </ul>
</div>
</div>
<div class="row">
<div class="col s12">
    <div class="input-field" style="margin-top: 0;">
        <a class="prefix"><i class="material-icons">message</i></a>
        <input @keyup.enter="sendMessage" id="message" type="text" class="validate" placeholder="type message here, and press Enter to send">
    </div>
</div>
</div>
</div>`,
    data: function() {
        return {
            messageList: []
        }
    },
    methods: {
        sendMessage: function() {
            let user = firebase.auth().currentUser;
            let message = $('#message').val();
            let currentTime = firebase.database.ServerValue.TIMESTAMP;
            if (message !== '') {
                firebase.database().ref('/chat').push({
                    id: user.uid + '-' + currentTime.toString(),
                    user: user.uid,
                    message: message,
                    postTime: currentTime
                }, function(error) {
                    if (error) {
                        Materialize.toast('送出訊息失敗', 4000, 'red');
                    }
                });
                $('#message').val('');
            }
        },
        scrollToBottom: function() {
            $('#message-list').scrollTop($('#message-list')[0].scrollHeight);
        }
    },
    beforeMount: function() {
        let user = firebase.auth().currentUser;
        if (user === null) {
            this.$root.page = 'signin';
        }
    },
    created: function(){
        let user = firebase.auth().currentUser;
        let component = this;
        firebase.database().ref('/users/' + user.uid).on('value', function (snapshot) {
            //component.username = snapshot.val().username;
        });

        firebase.database().ref('/chat').orderByChild('postTime').on('child_added', function(snapshot) {
            message = snapshot.val();
            component.messageList.push(message);
        });
    },
    updated: function() {
        this.scrollToBottom();
    }
});