<template>
    <div class="row">
        <h3>Hello! This is template page!</h3>
        <div class="leftOfScreen col-5">
            <h5>Left of scren</h5>
            <q-btn label="clear interval" @click="clear"/>
            <div>
                <input
                    v-model="chatName"
                    placeholder="Input name for new chat"
                />
                <q-btn
                    label="create"
                    @click="createChatroom"
                />
            </div>
            <div class="chatListDisplay">
                <div
                    v-for="(chat, i) in chatroomList"
                    :key="i"
                    class="chatroomCard row"
                    outline
                >
                    <p class="col-9">{{ chat.name }}</p>
                    <p>Chatroom id: {{ chat._id }}</p>
                    <button
                        class="enterChatBtn"
                        @click="initChat(chat._id)"
                    >
                        Enter chatroom
                    </button>
                </div>
            </div>
            <div class="displayField">
                <h5>showingDocument</h5>
                <p> {{ showingDocument }} </p>
            </div>
            <div class="displayField">
                <h5>Result Text</h5>
                <p> {{ resultText }} </p>
            </div>
            <div class="displayField">
                <h5>Chatroom List</h5>
                <p v-for="chat in chatroomList" :key="chat._id">
                    {{ chat }}
                </p>
            </div>
        </div>
        <div class="rightOfScreen col-7">
            <h5>Msgs show here</h5>
            <div class="MSGdisplayField">
                <p v-for="msg in msgList" :key="msg.timeStamp">
                    {{ msg.name }} : {{ msg.message }}
                    <br>
                    ({{ displayTime(msg.timeStamp) }})
                </p>
            </div>
            <input
                placeholder="Enter message"
                v-model="message"
            />
            <q-btn
                label="send"
                @click="sendMsg"
                :disabled="isSendDisabled"
            />
            <div
                class="userNameSelection"
                v-for="(user, i) in userList"
                :key="i"
            >
                <input type="radio" :id="user.name" :value="user.name" v-model="userName" />
                <label :for="user.name">{{ user.name }}</label>
            </div>
            <hr>
            <div
                class="chatSelection"
                v-for="chat in chatroomList"
                :key="chat._id"
            >
                <input type="radio" :id="chat.name" :value="chat._id" v-model="chosenChatroom" />
                <label :for="chat.name">{{ chat.name }}</label>
            </div>
            <q-btn
                label="test get msg"
                @click="getMsgs"
                :disabled="isGetMsgDisabled"
            />
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
    computed: {
        isSendDisabled() {
            return !(this.userName !== "" && this.message !== "" && this.chosenChatroom !== undefined);
        },
        isGetMsgDisabled() {
            return this.chosenChatroom === undefined;
        },
        showingDocument() {
            const document = {
                name: this.userName,
                message: this.message,
                chatroomId: this.chosenChatroom,
                timeStamp: Date.now()
            };
            return document;
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
        clear() {
            clearInterval(this.autoUpdateIntervalID);
        },
        displayTime(unix) {
            return (new Date(unix).toLocaleString("en-GB"));
        },
        propClick(name) {
            this.resultText = `Click! on ${name}`;
        },
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
                    this.resultText = error;
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
                    this.resultText = error;
                });
        },
        initChat(chatId) {
            this.$api.get(`api/init_chat/${chatId}`)
                .then(response => {
                    this.chosenChatroom = chatId;
                    this.msgList = response.data;
                })
                .catch(error => {
                    this.resultText = error;
                });
        },
        getMsgs() {
            console.log("get msgs");
            if (this.msgList.length === 0) {
                console.log("there is no msg in this chatroom!");
                this.initChat(this.chosenChatroom);
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
                    this.resultText = error;
                });
        },
        insertManyAndGetAll() {
            this.$api.post("api/test_insert_many", { range: 5 })
                .then(response => {
                    this.resultText = response.data;
                    return this.$api.get("api/get_all_msg");
                })
                .catch(error => {
                    this.resultText = error;
                })
                .then(getResponse => {
                    this.resultText = getResponse.data;
                })
                .catch(error => {
                    this.resultText = error;
                });
        },
        testSort() {
            this.$api.post("api/test_insert_many", { range: 5 })
                .then(response => {
                    console.log(response.data);
                    return this.$api.get("api/test_get_many_sort");
                })
                .catch(error => {
                    console.error("error inserting");
                    console.error(error);
                })
                .then(getResponse => {
                    console.log(getResponse.data);
                })
                .catch(error => {
                    console.error("error getting many");
                    console.error(error);
                });
        },
        testFindOne() {
            // passed
            // in actual application in chatroom, msg_id will be chatroom_id instead
            // and will be finding all documents in the same collection with the same chatroom_id
            this.$api.get(`api/find_one/${this.resultText.msg_id}`)
                .then(response => {
                    console.log(response);
                    this.findOneResult = response.data;
                })
                .catch(error => {
                    this.findOneResult = error;
                });
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
                this.resultText = `created( ) gets ${error}`;
            });
    }
};
</script>

<style scoped>
.displayField {
    border: 2px solid #93a1a1;
    border-radius: 10px;
    padding: 1%;
    min-height: 6em;
    max-width: 80%
}
.MSGdisplayField {
    border: 2px solid #93a1a1;
    border-radius: 10px;
    padding: 1%;
    min-height: 6em;
    max-height: 12em;
    max-width: 80%;
    overflow-y: scroll;
}
.chatListDisplay {
    border: 2px solid #93a1a1;
    border-radius: 10px;
    padding: 1% 1% 2% 1%;
    min-height: 6em;
    max-width: 80%;
    margin: 0% 0% 5% 0%
}
.chatroomCard {
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
.rightOfScreen {
    border-left: 1px solid #000D11;
    padding: 0% 0% 0% 2%
}
</style>
