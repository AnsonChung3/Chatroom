<template>
    <div>
        <p
            v-for="msg in msgList"
            :key="msg._id"
        >
            {{ msg.name }} : {{ msg.message }}
            <br>
            ({{ displayTime(msg.timeStamp) }})
        </p>
    </div>
</template>

<script>
export default {
    props: {
        msgList: {
            required: true
        }
    },
    data() {
        return {};
    },
    methods: {
        displayTime(unix) {
            return (new Date(unix).toLocaleString("en-GB"));
        }
    }
};
</script>

<style scoped>
p {
    font-size: 1.2vw
}
</style>
