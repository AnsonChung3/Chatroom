<template>
    <div class="chatroom-top-level-css">
        <q-dialog v-model="customAlert">
            <q-card class="customElementHighlighting">
                <q-card-section>
                    <p>{{ customAlertText }}</p>
                </q-card-section>

                <q-card-actions align="right">
                    <q-btn
                        @click="!customAlert"
                        v-close-popup
                        label="ok"
                        outline
                    />
                </q-card-actions>
            </q-card>
        </q-dialog>
        <h1>Welcome to Anson's chatroom!</h1>
        <div class="row">
            <div class="leftOfScreen col-5">
                <h2>List of Chatrooms</h2>
                <div class="chatroomList">
                    <div
                        v-if="isChatroomListEmpty"
                        class="chatroomListDisplayCard"
                    >
                        <p>Chat list initializing, just a moment...</p>
                    </div>
                    <div
                        v-else
                        v-for="chat in chatroomList"
                        :key="chat._id"
                        class="chatroomListDisplayCard row"
                        outline
                    >
                        <p class="col-9">{{ chat.name }}</p>
                        <button
                            class="customElementHighlighting"
                            @click="enterChatroom(chat._id)"
                        >
                            Enter chatroom
                        </button>
                    </div>
                </div>
                <div>
                    <input
                        v-model="chatroomName"
                        placeholder="Or, make a new one"
                    />
                    <q-btn
                        label="create"
                        @click="createChatroom"
                        outline
                    />
                </div>
            </div>
            <div class="rightOfScreen col">
                <h2 v-if="!chosenChatroom">Join a chat!</h2>
                <h2 v-else> You are in: {{ activeChatroom }}</h2>
                <div v-if="!userConfirmed">
                    <p>
                        First things first! Please input your name before joining any chat.<br>
                        Beware! <span style="font-weight: bold">Once confirmed, this can't be changed.</span>
                    </p>
                    <input
                        v-model="userName"
                        placeholder="What's your name?"
                    />
                    <q-btn
                        label="confirm"
                        @click="confirmUserName"
                        outline
                    />
                </div>
                <div v-else>
                    <div class="msgDisplayField">
                        <p v-if="!chosenChatroom"> You are not in a chatroom yet </p>
                        <p
                        <p v-else-if="isMsgListEmpty"> Hooray! You are the first person who gets here! Say something!</p>
                            v-else
                            v-for="msg in msgList"
                            :key="msg.timeStamp + msg.name"
                        >
                            {{ msg.name }} : {{ msg.message }}
                            <br>
                            ({{ displayTime(msg.timeStamp) }})
                        </p>
                    </div>
                    <input
                        :placeholder="msgInputPlaceholder"
                        v-model="message"
                    />
                    <q-btn
                        label="send"
                        @click="sendMsg"
                        :disabled="isSendDisabled"
                        outline
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            chatroomName: "",
            userName: "",
            message: "",
            chatroomList: [],
            msgList: [],
            chosenChatroom: undefined,
            autoUpdateIntervalID: undefined,
            userConfirmed: false,
            customAlert: false,
            customAlertText: ""
        };
    },
    computed: {
        isChatroomListEmpty() {
            return (this.chatroomList.length === 0);
        },
        isMsgListEmpty() {
            return (this.msgList.length === 0);
        },
        isSendDisabled() {
            return (this.userName === "" || this.message === "" || this.chosenChatroom === undefined);
        },
        activeChatroom() {
            return this.chatroomList.find(chat => chat._id === this.chosenChatroom).name;
        },
        msgInputPlaceholder() {
            return `${this.userName} says...`;
        }
    },
    watch: {
        chosenChatroom() {
            if (this.autoUpdateIntervalID !== undefined) {
                clearInterval(this.autoUpdateIntervalID);
            }
            this.autoUpdateIntervalID = setInterval(this.getMsgs, 1000);
        }
    },
    methods: {
        createChatroom() {
            if (this.chatroomName.length > 20) {
                this.customAlert = true;
                this.customAlertText = "Sorry mate, need to trim your cool name down to 20 characters.";
                return;
            }
            const chatName = (this.chatroomName === "") ? "Anson's Default Chatroom" : this.chatroomName;
            this.chatroomName = "";
            const document = {
                name: chatName
            };
            this.$api.post("api/create_chatroom", { document })
                .then(response => {
                    document._id = response.data;
                    this.chatroomList.push(document);
                })
                .catch(error => {
                    console.log(error);
                });
        },
        enterChatroom(chatId) {
            if (this.userConfirmed === false) {
                this.emptyUserNameAlert = true;
                return;
            }
            // this is to prevent repeat entrance of the same chatroom
            if (chatId === this.chosenChatroom) {
                return;
            }
            this.$api.get(`api/get_msgs/${chatId}`)
                .then(response => {
                    // on success, updating this.chosenChatroom triggers the watcher for auto update
                    // replace this.msgList as a whole regardless of empty chatroom or not
                    this.chosenChatroom = chatId;
                    this.msgList = response.data;
                })
                .catch(error => {
                    console.log(error);
                });
        },
        sendMsg() {
            const document = {
                name: this.userName,
                message: this.message,
                chatroomId: this.chosenChatroom,
                timeStamp: Date.now()
            };
            this.$api.post("api/send_msg", { document })
                .then(response => {
                    this.message = "";
                })
                .catch(error => {
                    console.log(error);
                });
        },
        getMsgs() {
            const latestTimeStampInChat = (this.msgList.length === 0) ? 0 : this.msgList[this.msgList.length - 1].timeStamp;
            this.$api.get(`api/get_msgs/${this.chosenChatroom}?timeStamp=${latestTimeStampInChat}`)
                .then(response => {
                    response.data.forEach(msg => this.msgList.push(msg));
                })
                .catch(error => {
                    console.log(error);
                });
        },
        clear() {
            clearInterval(this.autoUpdateIntervalID);
        confirmUserName() {
            if (this.userName === "") {
                this.customAlert = true;
                this.customAlertText = "Think of a cool name before barging in!";
                return;
            }
            if (this.userName.length > 10) {
                this.customAlert = true;
                this.customAlertText = "Calm down, cool person. Trim your coolness down to 10 characters please.";
                return;
            }
            this.userConfirmed = true;
        },
        },
        displayTime(unix) {
            return (new Date(unix).toLocaleString("en-GB"));
        }
    },
    created() {
        this.$api.get("api/get_chatrooms")
            .then(response => {
                if (response.data.length === 0) {
                    this.createChatroom();
                }
                this.chatroomList = Object.values(response.data);
            })
            .catch(error => {
                console.log(error);
            });
    }
};
</script>

<style scoped>
h1 {
    font-size: 5vw;
    margin: 2% 0% 2% 0%
}
h2 {
    font-size: 3vw;
    margin: 5px 0px 5px 0px
}
p {
    font-size: 1vw
}
input {
    margin: 0px 10px 0px 0px;
    width: 20em;
    font-size: 1vw
}
.chatroom-top-level-css {
    height: 100%;
    box-sizing: border-box;
    overflow: auto
}
.leftOfScreen {
    padding-left: 1%
}
.rightOfScreen {
    padding-left: 2%
}
.chatroomList {
    border: 2px solid #93a1a1;
    border-radius: 10px;
    padding: 0.5%;
    margin: 10px 0px 10px 0px;
    height: 20em;
    width: 95%;
    overflow: auto
}
.chatroomListDisplayCard {
    background: #003847;
    padding: 1% 1% 1% 3%;
    margin: 0.3vw;
    overflow-wrap: break-word;
    hyphens: auto
}
.msgDisplayField {
    border: 2px solid #93a1a1;
    border-radius: 10px;
    margin: 10px 0px 10px 0px;
    padding: 1%;
    height: 20em;
    max-width: 80%;
    overflow-y: auto;
    overflow-wrap: break-word;
    hyphens: auto
}
.customElementHighlighting {
    background: #00212B;
    color: #93a1a1;
    border: 1px solid #93a1a1;
    border-radius: 5px
}
</style>
