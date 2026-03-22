<template>
  <div class="message-input">
    <div class="username-row">
      <input 
        type="text" 
        :value="username"
        @input="$emit('usernameChange', $event.target.value)"
        placeholder="Your name"
        class="username-input"
      />
    </div>
    <div class="input-row">
      <input 
        type="text" 
        v-model="message"
        @keyup.enter="handleSend"
        placeholder="Type your message..."
        :disabled="disabled"
        class="message-input-field"
      />
      <button 
        @click="handleSend" 
        :disabled="disabled || !message.trim()"
        class="btn-send"
      >
        Send
      </button>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'MessageInput',
  props: {
    disabled: Boolean,
    username: String
  },
  emits: ['send', 'usernameChange'],
  setup(props, { emit }) {
    const message = ref('')

    const handleSend = () => {
      if (message.value.trim()) {
        emit('send', message.value.trim())
        message.value = ''
      }
    }

    return {
      message,
      handleSend
    }
  }
}
</script>

<style scoped>
.message-input {
  background: #16213e;
  padding: 15px;
  border-radius: 8px;
}

.username-row {
  margin-bottom: 10px;
}

.username-input {
  width: 100%;
  padding: 8px;
  border: none;
  border-radius: 4px;
  background: #0f3460;
  color: #fff;
  font-size: 14px;
}

.username-input::placeholder {
  color: #888;
}

.input-row {
  display: flex;
  gap: 10px;
}

.message-input-field {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 4px;
  background: #0f3460;
  color: #fff;
  font-size: 14px;
}

.message-input-field::placeholder {
  color: #888;
}

.message-input-field:disabled {
  opacity: 0.5;
}

.btn-send {
  padding: 12px 24px;
  background: #00d9ff;
  color: #1a1a2e;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  font-size: 14px;
}

.btn-send:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
