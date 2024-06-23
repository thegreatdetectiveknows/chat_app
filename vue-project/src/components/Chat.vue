<template>
  <div>
    <h1>Chat</h1>
    <div class="chat-window">
      <div v-for="message in messages" :key="message._id" class="message">
        <strong>{{ message.sender_id }}:</strong> {{ message.message_text }}
      </div>
    </div>
    <SendMessage @messageSent="fetchMessages" />
  </div>
</template>

<script>
import SendMessage from './SendMessage.vue';
import axios from 'axios';

export default {
  components: {
    SendMessage
  },
  data() {
    return {
      messages: []
    };
  },
  methods: {
    async fetchMessages() {
      try {
        const response = await axios.get('http://localhost:8002/messages');
        this.messages = response.data;
      } catch (error) {
        console.error('Error fetching messages:', error);
      }
    }
  },
  mounted() {
    this.fetchMessages();
  }
};
</script>

<style>
.chat-window {
  border: 1px solid #ccc;
  padding: 10px;
  height: 300px;
  overflow-y: scroll;
}

.message {
  margin-bottom: 10px;
}
</style>
