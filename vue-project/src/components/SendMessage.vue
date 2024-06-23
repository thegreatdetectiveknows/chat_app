<template>
    <div>
      <h2>Send Message</h2>
      <form @submit.prevent="sendMessage">
        <div>
          <label for="chat_id">Chat ID:</label>
          <input type="text" v-model="message.chat_id" required />
        </div>
        <div>
          <label for="message_text">Message:</label>
          <input type="text" v-model="message.message_text" required />
        </div>
        <button type="submit">Send</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
  data() {
    return {
      message: {
        chat_id: '',
        message_text: '',
        date: new Date().toISOString(),
        admin_id: 'admin123',  // Example admin ID
      }
    };
  },
  methods: {
    async sendMessage() {
      try {
        const response = await axios.post('http://localhost:8002/messages/from_admin', this.message);
        alert('Message sent!');
      } catch (error) {
        console.error('Error sending message:', error);
      }
    }
  }
};
  </script>
  