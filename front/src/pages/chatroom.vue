<template>
    <div class="chatroom-top-level-css">
        <h1>Welcome to Anson's chatroom!</h1>
        <div class="row">
            <div class="leftOfScreen col-5">
                <div v-if="!userConfirmed">
                    <p>
                        First things first! Please input your name before joining any chat.<br>
                        Beware! <span style="font-weight: bold">Once confirmed, this can't be changed.</span>
                    </p>
                    <input
                        v-model="userName"
                        placeholder="What's your name?"
                        style="margin: 0% 2% 0% 0%; width: 20em"
                    />
                    <q-btn
                        label="confirm"
                        @click="confirmUserName"
                        outline
                    />
                </div>
                <div v-else>
                    <p>Hello, {{ userName }}! Come join our chat!</p>
                </div>
                <h2>List of Chatrooms</h2>
                <div>
                    <input
                        v-model="chatroomName"
                        placeholder="Input name for new chatroom"
                        style="margin: 0% 2% 2% 0%; width: 20em"
                    />
                    <q-btn
                        label="create"
                        @click="createChatroom"
                        outline
                    />
                </div>
                <div class="containChatroomList">
                    <div class="chatroomList">
                        <div
                            v-if="chatroomListEmpty"
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
                                class="enterChatroomBtn"
                                @click="enterChatroom(chat._id)"
                            >
                                Enter chatroom
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            <div class="rightOfScreen col">
                <h2 v-if="!chosenChatroom">Join a chat!</h2>
                <h2 v-else> You are in: {{ activeChatroom }}</h2>
                <div class="msgDisplayField">
                    <p v-if="!chosenChatroom"> You are not in a chatroom yet </p>
                    <p v-else-if="msgListEmpty"> Hooray! You are the first person who gets here! Say something!</p>
                    <p
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
                    placeholder="Enter message"
                    v-model="message"
                    style="margin: 2% 2% 0% 0%; width: 20em"
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
            userConfirmed: false
        };
    },
    computed: {
        chatroomListEmpty() {
            return (this.chatroomList.length === 0);
        },
        msgListEmpty() {
            return (this.msgList.length === 0);
        },
        isSendDisabled() {
            return (this.userName === "" || this.message === "" || this.chosenChatroom === undefined);
        },
        activeChatroom() {
            return this.chatroomList.find(chat => chat._id === this.chosenChatroom).name;
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
        confirmUserName() {
            this.userConfirmed = true;
        },
        createChatroom() {
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
            this.$api.get(`api/get_msgs/${chatId}`)
                .then(response => {
                    this.chosenChatroom = chatId;
                    response.data.forEach(msg => this.msgList.push(msg));
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
.containChatroomList {
    overflow-y: auto;
    max-height: 25em
}
.chatroomList {
    border: 2px solid #93a1a1;
    border-radius: 10px;
    padding: 1% 1% 2% 1%;
    min-height: 6em;
    max-width: 80%;
    margin: 5% 0% 5% 0%;
}
.chatroomListDisplayCard {
    background: #003847;
    padding: 1% 1% 1% 3%;
    margin: 5px 2px 0px 2px
}
.enterChatroomBtn {
    background: #00212B;
    color: #93a1a1;
    border: 1px solid #93a1a1;
    border-radius: 5px
}
.msgDisplayField {
    border: 2px solid #93a1a1;
    border-radius: 10px;
    padding: 1%;
    height: 20em;
    max-width: 80%;
    overflow-y: auto;
}
.rightOfScreen {
    padding: 0% 0% 0% 2%
}
</style>
