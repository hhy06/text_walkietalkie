<template>
  <div class="app">
    <header>
      <h1>Text Walkie Talkie</h1>
    </header>
    <ConnectionPanel 
      :serverConfig="serverConfig"
      :isConnected="isConnected"
      :connectionError="connectionError"
      @connect="connect"
      @disconnect="disconnect"
    />
    <MessageDialogue :messages="messages" :currentUsername="currentUsername" />
    <MessageInput 
      :disabled="!isConnected"
      :username="currentUsername"
      @send="sendMessage"
      @usernameChange="updateUsername"
    />
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import ConnectionPanel from './components/ConnectionPanel.vue'
import MessageDialogue from './components/MessageDialogue.vue'
import MessageInput from './components/MessageInput.vue'

export default {
  name: 'App',
  components: {
    ConnectionPanel,
    MessageDialogue,
    MessageInput
  },
  setup() {
    const serverConfig = ref({
      host: '',
      port: 5000
    })
    const isConnected = ref(false)
    const connectionError = ref('')
    const messages = ref([])
    const currentUsername = ref(localStorage.getItem('walkietalkie_username') || '')
    let pollInterval = null

    const loadSavedConfig = () => {
      const saved = localStorage.getItem('walkietalkie_servers')
      if (saved) {
        const servers = JSON.parse(saved)
        if (servers.length > 0) {
          serverConfig.value = servers[0]
        }
      }
    }

    const saveServerConfig = () => {
      const saved = localStorage.getItem('walkietalkie_servers')
      let servers = saved ? JSON.parse(saved) : []
      const existing = servers.findIndex(s => 
        s.host === serverConfig.value.host && s.port === serverConfig.value.port
      )
      if (existing >= 0) {
        servers.splice(existing, 1)
      }
      servers.unshift({ ...serverConfig.value })
      servers = servers.slice(0, 5)
      localStorage.setItem('walkietalkie_servers', JSON.stringify(servers))
    }

    const getBaseUrl = () => {
      return `http://${serverConfig.value.host}:${serverConfig.value.port}`
    }

    const checkConnection = async () => {
      try {
        const response = await fetch(`${getBaseUrl()}/api/status`)
        if (response.ok) {
          isConnected.value = true
          connectionError.value = ''
          saveServerConfig()
          return true
        }
      } catch (e) {
        return false
      }
      isConnected.value = false
      return false
    }

    const fetchMessages = async () => {
      try {
        const response = await fetch(`${getBaseUrl()}/api/messages?limit=100`)
        if (response.ok) {
          const data = await response.json()
          messages.value = data.messages
        }
      } catch (e) {
        console.error('Failed to fetch messages:', e)
      }
    }

    const startPolling = () => {
      fetchMessages()
      pollInterval = setInterval(fetchMessages, 2000)
    }

    const stopPolling = () => {
      if (pollInterval) {
        clearInterval(pollInterval)
        pollInterval = null
      }
    }

    const connect = async (config) => {
      serverConfig.value = config
      const connected = await checkConnection()
      if (connected) {
        startPolling()
      } else {
        connectionError.value = 'Failed to connect to server'
      }
    }

    const disconnect = () => {
      stopPolling()
      isConnected.value = false
      messages.value = []
    }

    const sendMessage = async (content) => {
      if (!isConnected.value || !currentUsername.value) return
      
      try {
        const response = await fetch(`${getBaseUrl()}/api/messages`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: currentUsername.value,
            content: content
          })
        })
        if (response.ok) {
          fetchMessages()
        }
      } catch (e) {
        console.error('Failed to send message:', e)
      }
    }

    const updateUsername = (name) => {
      currentUsername.value = name
      localStorage.setItem('walkietalkie_username', name)
    }

    onMounted(() => {
      loadSavedConfig()
    })

    onUnmounted(() => {
      stopPolling()
    })

    return {
      serverConfig,
      isConnected,
      connectionError,
      messages,
      currentUsername,
      connect,
      disconnect,
      sendMessage,
      updateUsername
    }
  }
}
</script>

<style>
.app {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  height: 100vh;
}

header {
  text-align: center;
  margin-bottom: 20px;
}

header h1 {
  font-size: 24px;
  color: #00d9ff;
}
</style>
