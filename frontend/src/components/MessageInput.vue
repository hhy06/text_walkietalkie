<template>
  <div class="message-input">
    <div class="username-row">
      <div class="dropdown-wrapper">
        <input 
          type="text" 
          :value="username"
          @input="$emit('usernameChange', $event.target.value)"
          @focus="showDropdown = true"
          @blur="hideDropdownDelayed"
          placeholder="Your name"
          class="username-input"
        />
        <span class="dropdown-arrow" @click="toggleDropdown">▼</span>
        <div v-if="showDropdown && savedUsernames && savedUsernames.length > 0" class="custom-dropdown">
          <div 
            v-for="name in savedUsernames" 
            :key="name"
            class="dropdown-item"
            @mousedown.prevent="selectUsername(name)"
          >
            {{ name }}
          </div>
        </div>
      </div>
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
    username: String,
    savedUsernames: {
      type: Array,
      default: () => []
    }
  },
  emits: ['send', 'usernameChange'],
  setup(props, { emit }) {
    const message = ref('')
    const showDropdown = ref(false)

    const hideDropdown = () => {
      showDropdown.value = false
    }

    const hideDropdownDelayed = () => {
      setTimeout(() => {
        showDropdown.value = false
      }, 200)
    }

    const toggleDropdown = () => {
      showDropdown.value = !showDropdown.value
    }

    const selectUsername = (name) => {
      emit('usernameChange', name)
      showDropdown.value = false
    }

    const handleSend = () => {
      if (message.value.trim()) {
        emit('send', message.value.trim())
        message.value = ''
      }
    }

    return {
      message,
      showDropdown,
      handleSend,
      hideDropdown,
      hideDropdownDelayed,
      toggleDropdown,
      selectUsername
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

.dropdown-wrapper {
  position: relative;
}

.username-input {
  width: 100%;
  padding: 8px 30px 8px 8px;
  border: none;
  border-radius: 4px;
  background: #0f3460;
  color: #fff;
  font-size: 14px;
  box-sizing: border-box;
}

.username-input::placeholder {
  color: #888;
}

.dropdown-arrow {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: #888;
  cursor: pointer;
  font-size: 10px;
  user-select: none;
}

.custom-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: #0f3460;
  border-radius: 4px;
  margin-top: 4px;
  max-height: 150px;
  overflow-y: auto;
  z-index: 100;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

.dropdown-item {
  padding: 8px 12px;
  cursor: pointer;
  color: #fff;
  font-size: 14px;
}

.dropdown-item:hover {
  background: #1a4a7a;
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
