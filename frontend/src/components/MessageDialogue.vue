<template>
  <div class="message-dialogue-wrapper">
    <div class="toolbar">
      <button @click="exportMessages" class="btn-export" :disabled="messages.length === 0">
        📥 Export
      </button>
    </div>
    <div class="message-dialogue" ref="dialogueRef">
      <div v-if="messages.length === 0" class="empty-state">
        No messages yet. Start the conversation!
      </div>
      <div 
        v-for="msg in messages" 
        :key="msg.id"
        :class="['message', { 'own-message': msg.username === currentUsername }]"
      >
        <div class="message-header">
          <span class="username">{{ msg.username }}</span>
          <span class="timestamp">{{ formatTime(msg.timestamp) }}</span>
        </div>
        <div class="message-content">{{ msg.content }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch, nextTick } from 'vue'

export default {
  name: 'MessageDialogue',
  props: {
    messages: Array,
    currentUsername: String
  },
  setup(props) {
    const dialogueRef = ref(null)

    const formatTime = (timestamp) => {
      const date = new Date(timestamp)
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }

    const formatFullTimestamp = (timestamp) => {
      const date = new Date(timestamp)
      return date.toISOString().replace('T', ' ').slice(0, 19)
    }

    const exportMessages = () => {
      if (props.messages.length === 0) return

      const lines = props.messages.map(msg => {
        return `[${formatFullTimestamp(msg.timestamp)}] ${msg.username}: ${msg.content}`
      })

      const content = `Text Walkie Talkie Export
Exported: ${new Date().toISOString().replace('T', ' ').slice(0, 19)}
Total messages: ${props.messages.length}
${'='.repeat(50)}

${lines.join('\n')}`

      const blob = new Blob([content], { type: 'text/plain;charset=utf-8' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `walkietalkie_export_${new Date().toISOString().slice(0,10)}.txt`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    }

    const scrollToBottom = () => {
      nextTick(() => {
        if (dialogueRef.value) {
          dialogueRef.value.scrollTop = dialogueRef.value.scrollHeight
        }
      })
    }

    watch(() => props.messages.length, () => {
      scrollToBottom()
    })

    return {
      dialogueRef,
      formatTime,
      exportMessages
    }
  }
}
</script>

<style scoped>
.message-dialogue-wrapper {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
}

.toolbar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 8px;
}

.btn-export {
  padding: 6px 12px;
  background: #0f3460;
  color: #00d9ff;
  border: 1px solid #00d9ff;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  font-weight: bold;
}

.btn-export:hover:not(:disabled) {
  background: #00d9ff;
  color: #1a1a2e;
}

.btn-export:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.message-dialogue {
  flex: 1;
  overflow-y: auto;
  background: #16213e;
  border-radius: 8px;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.empty-state {
  text-align: center;
  color: #888;
  margin-top: 50px;
}

.message {
  background: #0f3460;
  padding: 12px;
  border-radius: 8px;
  max-width: 80%;
}

.message.own-message {
  background: #00d9ff;
  color: #1a1a2e;
  margin-left: auto;
}

.message.own-message .username,
.message.own-message .timestamp {
  color: #1a1a2e;
}

.message-header {
  display: flex;
  justify-content: space-between;
  gap: 15px;
  margin-bottom: 5px;
}

.username {
  font-weight: bold;
  color: #00d9ff;
}

.own-message .username {
  color: #1a1a2e;
}

.timestamp {
  font-size: 12px;
  color: #888;
}

.message-content {
  word-wrap: break-word;
}
</style>
