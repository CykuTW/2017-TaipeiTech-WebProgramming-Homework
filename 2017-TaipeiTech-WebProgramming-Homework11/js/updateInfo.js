Vue.component('updateInfo', {
    template: `
<div class="container">
    <div class="row" />
    <div class="row" />
    <div class="row">
        <div class="col s12">
            <div class="card">
                <div class="card-content">
                    <span class="card-title">Update User Information</span>
                    <hr /><br /><br />
                    <div class="center">
                        <img :src="sticker" id="sticker-preview" style="width: 200px; height: 200px;" class="circle responsive-img">
                        <div class="file-field input-field" style="margin: auto; width: 50%">
                            <div class="btn">
                                <span>CHOOSE</span>
                                <input @change="previewSticker" id="sticker" type="file" accept="image/*">
                            </div>
                            <div class="file-path-wrapper">
                                <input class="file-path validate" type="text" placeholder="Upload your sticker...">
                            </div>
                        </div>
                    </div>
                    <br />
                    <div class="input-field">
                        <i class="material-icons prefix">account_circle</i>
                        <input v-model="username" id="username" type="text" class="validate">
                        <label for="username">User Name</label>
                    </div>
                    <div class="input-field">
                        <i class="material-icons prefix">business</i>
                        <input v-model="occupation" id="occupation" type="text" class="validate">
                        <label for="occupation">Occupation</label>
                    </div>
                    <div class="input-field">
                        <i class="material-icons prefix">cake</i>
                        <input v-model.number="age" id="age" type="number" min="0" class="validate">
                        <label for="age">Age</label>
                    </div>
                    <div class="input-field">
                        <i class="material-icons prefix">description</i>
                        <textarea v-on:keydown="resizeTextArea" v-model="description" id="description" class="materialize-textarea" style="height: 45px;"></textarea>
                        <label for="description">Description</label>
                    </div>
                </div>
                <div class="center">
                    <button @click="updateInfo" class="btn waves-effect waves-light">
                        SAVE
                        <i class="material-icons right">save</i>
                    </button>
                    <button @click="back" class="btn waves-effect waves-light">
                        BACK
                        <i class="material-icons right">exit_to_app</i>
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
            occupation: '',
            age: 0,
            description: '',
            sticker: ''
        }
    },
    methods: {
        resizeTextArea: function() {
            //修正 materializecss 的 textarea 沒有自動 resize 的 bug
            var textarea = $('#description').first();
            var hiddenDiv = $('.hiddendiv').first();
            if (hiddenDiv.length) {
                hiddenDiv.css('width', textarea.width());
                textarea.css('height', hiddenDiv.height());
            }
        },
        updateInfo: function() {
            let user = firebase.auth().currentUser;
            this.uploadSticker();
            firebase.database().ref('/users/' + user.uid).update({
                username: this.username,
                occupation: this.occupation,
                age: this.age,
                description: this.description
            }).then(function() {
                Materialize.toast('更新成功，趕快到聊天室玩玩看吧！', 4000, 'green');
            }).catch(function(error) {
                Materialize.toast('更新失敗', 4000, 'red');
            });
        },
        uploadSticker: function() {
            if ($('#sticker')[0].files.length!=0) {
                let component = this;
                let user = firebase.auth().currentUser;
                let sticker = $('#sticker')[0].files[0];
                $('#sticker').val('').change();
                firebase.storage().ref('/sticker/' + user.uid).put(sticker).then(function(snapshot) {
                    Materialize.toast('上傳大頭貼成功', 4000, 'green');
                    //$('#sticker-preview').attr('src', snapshot.downloadURL);
                    component.sticker = snapshot.downloadURL;
                }).catch(function(error) {
                    Materialize.toast('上傳大頭貼失敗', 4000, 'red');
                });
            }
        },
        back: function() {
            this.$root.page = 'info';
        },
        previewSticker: function() {
            let file = $('#sticker')[0].files[0];
            let component = this;
            if (FileReader && file) {
                var fr = new FileReader();
                fr.onload = function () {
                    component.sticker = fr.result;
                }
                fr.readAsDataURL(file);
            }
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
            component.username = snapshot.val().username;
            component.occupation = snapshot.val().occupation;
            component.age = snapshot.val().age;
            component.description = snapshot.val().description;
        });
        firebase.storage().ref('/sticker/' + user.uid).getDownloadURL().then(function(url) {
            //$('#sticker-preview').attr('src', url);
            component.sticker = url;
        }).catch(function(error) {
            firebase.storage().ref('/sticker/defaultSticker').getDownloadURL().then(function(url) {
                //$('#sticker-preview').attr('src', url);
                component.sticker = url;
            }).catch(function(error){});
        });
    },
    mounted: function() {
        $('input, textarea').change(); //trigger all material input animation
    }
});
