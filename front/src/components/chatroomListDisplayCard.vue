<template>
    <div>
        <div
            v-for="chat in chatroomList"
            :key="chat._id"
            class="row"
        >
            <p class="col-9">{{ chat.name }}</p>
            <button
                @click="$emit('enterChatroom', chat._id)"
                class="customElementHighlighting"
            >
                Enter chatroom
            </button>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        chatroomList: {
            required: true
        }
    },
    data() {
        return {};
    },
    methods: {}
};
</script>

<style scoped>
p {
    font-size: 1.2vw
}
.row {
    border-bottom: 2px solid #00212B;
    padding-bottom: 5px;
    margin-bottom: 5px
}
.customElementHighlighting {
    background: #00212B;
    color: #93a1a1;
    border: 1px solid #93a1a1;
    border-radius: 5px
}
</style>
