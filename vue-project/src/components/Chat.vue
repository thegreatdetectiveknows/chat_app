<template>
    <div class="chat">
      <div class="messages">
        <div v-for="msg in messages" :key="msg.messageId" class="message">
          <strong>{{ msg.sender }}:</strong> {{ msg.text }}
        </div>
      </div>
      <div class="input">
        <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="Type your message" />
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        messages: [],
        newMessage: '',
        userId: 'user123',
        sender: 'admin'
      };
    },
    methods: {
      async sendMessage() {
        if (this.newMessage.trim() === '') return;
  
        const message = {
          messageId: Date.now(),
          userId: this.userId,
          text: this.newMessage,
          sentAt: new Date().toISOString(),
          sender: this.sender
        };
  
        try {
          const response = await axios.post('http://localhost:8001/route_message', message);
          if (response.status === 200) {
            this.messages.push(message);
            this.newMessage = '';
          } else {
            console.error('Error sending message:', response.statusText);
          }
        } catch (error) {
          console.error('Error sending message:', error);
        }
      }
    }
  };
  </script>
  
  <style>
  .chat {
    width: 400px;
    margin: 0 auto;
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 5px;
  }
  .messages {
    height: 300px;
    overflow-y: auto;
    border-bottom: 1px solid #ccc;
    margin-bottom: 10px;
  }
  .message {
    margin: 5px 0;
  }
  .input input {
    width: 100%;
    padding: 10px;
    box-sizing: border-box;
  }
  </style>
  