<template>
  <div class="connection-panel">
    <div class="config-row">
      <input 
        type="text" 
        v-model="host" 
        placeholder="Server IP"
        @focus="showHistory = true"
      />
      <input 
        type="number" 
        v-model="port" 
        placeholder="Port"
      />
      <button v-if="!isConnected" @click="handleConnect" class="btn-connect">
        Connect
      </button>
      <button v-else @click="$emit('disconnect')" class="btn-disconnect">
        Disconnect
      </button>
    </div>
    <div v-if="showHistory && savedServers.length > 0" class="server-history">
      <div 
        v-for="server in savedServers" 
        :key="`${server.host}:${server.port}`"
        class="server-item"
        @click="selectServer(server)"
      >
        {{ server.host }}:{{ server.port }}
      </div>
    </div>
    <div v-if="connectionError" class="error">{{ connectionError }}</div>
    <div v-if="isConnected" class="status connected">Connected</div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'

export default {
  name: 'ConnectionPanel',
  props: {
    serverConfig: Object,
    isConnected: Boolean,
    connectionError: String
  },
  emits: ['connect', 'disconnect'],
  setup(props, { emit }) {
    const host = ref(props.serverConfig.host || '')
    const port = ref(props.serverConfig.port || 5000)
    const showHistory = ref(false)
    const savedServers = ref([])

    const loadSavedServers = () => {
      const saved = localStorage.getItem('walkietalkie_servers')
      if (saved) {
        savedServers.value = JSON.parse(saved)
      }
    }

    const handleConnect = () => {
      if (host.value && port.value) {
        showHistory.value = false
        emit('connect', { host: host.value, port: port.value })
      }
    }

    const selectServer = (server) => {
      host.value = server.host
      port.value = server.port
      showHistory.value = false
      emit('connect', { host: server.host, port: server.port })
    }

    onMounted(() => {
      loadSavedServers()
    })

    watch(() => props.serverConfig, (newConfig) => {
      host.value = newConfig.host
      port.value = newConfig.port
    }, { deep: true })

    return {
      host,
      port,
      showHistory,
      savedServers,
      handleConnect,
      selectServer
    }
  }
}
</script>

<style scoped>
.connection-panel {
  background: #16213e;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  position: relative;
}

.config-row {
  display: flex;
  gap: 10px;
}

input {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 4px;
  background: #0f3460;
  color: #fff;
  font-size: 14px;
}

input::placeholder {
  color: #888;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
}

.btn-connect {
  background: #00d9ff;
  color: #1a1a2e;
}

.btn-disconnect {
  background: #ff4757;
  color: #fff;
}

.server-history {
  position: absolute;
  top: 100%;
  left: 15px;
  right: 15px;
  background: #0f3460;
  border-radius: 4px;
  margin-top: 5px;
  z-index: 10;
  max-height: 200px;
  overflow-y: auto;
}

.server-item {
  padding: 10px;
  cursor: pointer;
  border-bottom: 1px solid #16213e;
}

.server-item:hover {
  background: #16213e;
}

.server-item:last-child {
  border-bottom: none;
}

.error {
  color: #ff4757;
  margin-top: 10px;
  font-size: 14px;
}

.status {
  margin-top: 10px;
  font-size: 14px;
  font-weight: bold;
}

.status.connected {
  color: #2ed573;
}
</style>
