Vue.component('info', {
    template: `
<div class="container">
    <div class="row" />
    <div class="row" />
    <div class="row">
        <div class="col s12">
            <div class="card">
                <div class="card-content">
                    <span class="card-title">User Information</span>
                    <hr /><br /><br />
                    <div class="center">
                        <img id="sticker-preview" style="width: 200px; height: 200px;" class="circle responsive-img">
                    </div>
                    <br />
                    <table class="centered">
                        <tbody>
                            <tr>
                                <th>User Name</th>
                                <td>{{username}}</td>
                            </tr>
                            <tr>
                                <th>E-Mail</th>
                                <td>{{email}}</td>
                            </tr>
                            <tr>
                                <th>Occupation</th>
                                <td>{{occupation}}</td>
                            </tr>
                            <tr>
                                <th>Age</th>
                                <td>{{age}}</td>
                            </tr>
                            <tr>
                                <th>Description</th>
                                <td>{{description}}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="center">
                    <button @click="gotoUpdateInfo" class="btn waves-effect waves-light">
                        UPDATE
                        <i class="material-icons right">update</i>
                    </button>
                    <br /><br /><br />
                </div>
            </div>
        </div>
    </div>
</div>`,
    data: function() {
        return {
            username: '',
            email: '',
            occupation: '',
            age: 0,
            description: ''
        }
    },
    methods: {
        gotoUpdateInfo: function() {
            this.$root.page = 'updateInfo';
        },
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
        firebase.database().ref('/users/' + user.uid).on('value', function(snapshot) {
            component.username = snapshot.val().username;
            component.occupation = snapshot.val().occupation;
            component.age = snapshot.val().age;
            component.description = snapshot.val().description;
            component.email = user.email;
        });

        firebase.storage().ref('/sticker/' + user.uid).getDownloadURL().then(function(url) {
            $('#sticker-preview').attr('src', url);
        }).catch(function(error) {
            firebase.storage().ref('/sticker/defaultSticker').getDownloadURL().then(function(url) {
                $('#sticker-preview').attr('src', url);
            }).catch(function(error){});
        });
    },
});