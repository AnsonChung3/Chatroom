<template>
    <div>
        <h3>Welcome to Anson's chatroom!</h3>
        <div class="row">
            <div class="leftOfScreen col-5">
                <h5>List of Chatrooms</h5>
                <div>
                    <input
                        v-model="chatName"
                        placeholder="Input name for new chat"
                        style="margin: 0% 2% 0% 0%; min-width: 20em"
                    />
                    <q-btn
                        label="create"
                        @click="createChatroom"
                        outline
                    />
                </div>
                <div class="containChatList">
                    <div class="chatList">
                        <div
                            v-for="(chat, i) in chatroomList"
                            :key="i"
                            class="chatListDisplayCard row"
                            outline
                        >
                            <p class="col-9">{{ chat.name }}</p>
                            <button
                                class="enterChatBtn"
                                @click="enterChat(chat._id)"
                            >
                                Enter chatroom
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            <div class="rightOfScreen col">
                <h5>right of screen</h5>
                <div class="msgDisplayField">
                    <p v-for="msg in msgList" :key="msg.timeStamp">
                        {{ msg.name }} : {{ msg.message }}
                        <br>
                        ({{ displayTime(msg.timeStamp) }})
                    </p>
                </div>
                <input
                    placeholder="Enter message"
                    v-model="message"
                    style="margin: 2% 2% 0% 0%; min-width: 20em"
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
            chatName: "",
            userName: "",
            message: "",
            chatroomList: [
                { name: "Anson" }, { name: "Nathan" }
            ],
            userList: [
                { name: "Anson" }, { name: "Nathan" }
            ],
            msgList: [],
            chosenChatroom: undefined,
            resultText: "Defualt result text here",
            autoUpdateIntervalID: undefined
        };
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
            const chatName = (this.chatName === "") ? "Anson's Default Chatroom" : this.chatName;
            this.chatName = "";
            const document = {
                name: chatName
            };
            this.$api.post("api/create_chatroom", { document })
                .then(response => {
                    document._id = response.data;
                    console.log("create chatroom, on succes, get response, overwrite result text");
                    this.resultText = document;
                    this.chatroomList.push(document);
                })
                .catch(error => {
                    console.log(error);
                });
        },
        enterChat(chatId) {
            this.$api.get(`api/enter_chat/${chatId}`)
                .then(response => {
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
            // variable document is passd in as payload
            // however, it needs to be inside a set of curly braces
            // this is short hand for { document: document} sicne key:value is the same
            // this.$api.post("api/insert_msg", { document })
            this.$api.post("api/send_msg", { document })
                .then(response => {
                    // on success, backend should return str(result.inserted_id)
                    // but this is useless for the actual app
                    // it's only here to let know of success
                    this.resultText = `msg : "${document.message}" is sent.`;
                    this.message = "";
                })
                .catch(error => {
                    console.log(error);
                });
        },
        getMsgs() {
            if (this.msgList.length === 0) {
                this.enterChat(this.chosenChatroom);
                return;
            }
            const latestTimeStampInChat = this.msgList[this.msgList.length - 1].timeStamp;
            this.$api.get(`api/get_msgs/${this.chosenChatroom}/${latestTimeStampInChat}`)
                .then(response => {
                    // response.data is an array
                    // problem now is to make sure i only get new msgs from the backend
                    // so latest updates
                    // and put it at the beginning of the array, so array.unshift()
                    // this.resultText = response.data;
                    // this.msgList = response.data;
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
                // there should be an if check, see if there is any set up chatroom
                // since i don't always restart the mongodb container
                // if there is nothing in the chatroom collection
                // here should be the place to create a default one
                if (response.data.length === 0) {
                    this.createChatroom();
                }
                // reponse.data is object, Object.values() returns an array of a given object's property values
                this.chatroomList = Object.values(response.data);
            })
            .catch(error => {
                console.log(error);
            });
    }
};
</script>

<style scoped>
.containChatList {
    overflow-y: auto;
    max-height: 50vw
}
.chatList {
    border: 2px solid #93a1a1;
    border-radius: 10px;
    padding: 1% 1% 2% 1%;
    min-height: 6em;
    max-width: 80%;
    margin: 5% 0% 5% 0%
}
.chatListDisplayCard {
    background: #003847;
    padding: 1% 1% 1% 3%;
    margin: 5px 2px 0px 2px
}
.enterChatBtn {
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
