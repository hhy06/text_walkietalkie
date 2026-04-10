<template>
  <div class="connection-panel">
    <div class="config-row">
      <input 
        type="text" 
        v-model="host" 
        placeholder="Server IP"
        list="server-history-list"
      />
      <datalist id="server-history-list">
        <option v-for="server in savedServers" :key="`${server.host}:${server.port}`" :value="server.host"></option>
      </datalist>
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
    const host = ref(props.serverConfig.host || 'localhost')
    const port = ref(props.serverConfig.port || 12358)
    const savedServers = ref([])

    const getCookie = (name) => {
      const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
      if (match) return decodeURIComponent(match[2]);
      return null;
    }

    const loadSavedServers = () => {
      const saved = getCookie('walkietalkie_servers')
      if (saved) {
        savedServers.value = JSON.parse(saved)
      }
    }

    const handleConnect = () => {
      if (host.value && port.value) {
        emit('connect', { host: host.value, port: port.value })
      }
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
      savedServers,
      handleConnect
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
