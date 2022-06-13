<template>
    <div>
        <h3>Welcome to Anson's chatroom!</h3>
        <div class="row">
            <div class="leftOfScreen col">
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
                </div>
            </div>
            <div class="rightOfScreen col">
                <h5>right of screen</h5>
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
        return {};
    },
    methods: {}
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
    overflow-y: auto;
}
.chatListDisplay {
    border: 2px solid #93a1a1;
    border-radius: 10px;
    padding: 1% 1% 2% 1%;
    min-height: 6em;
    max-width: 80%;
    margin: 5% 0% 5% 0%
}
.containChatList {
    overflow-y: auto;
    max-height: 50vw
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
    padding: 0% 0% 0% 2%;
}
</style>
