<template>
  <div class="connection-panel">
    <div class="config-row">
      <div class="dropdown-wrapper">
        <input 
          type="text" 
          v-model="host" 
          placeholder="Server IP"
          @focus="showHostDropdown = true"
          @blur="hideDropdownsDelayed"
        />
        <span class="dropdown-arrow" @click="toggleHostDropdown">▼</span>
        <div v-if="showHostDropdown && (savedHosts.length > 0 || probing)" class="custom-dropdown">
          <div v-if="probing" class="dropdown-item probing">Scanning LAN...</div>
          <div 
            v-for="item in savedHosts" 
            :key="item"
            class="dropdown-item"
            @mousedown.prevent="selectHost(item)"
          >
            {{ item }}
          </div>
          <div 
            v-for="item in discoveredServers" 
            :key="item"
            class="dropdown-item discovered"
            @mousedown.prevent="selectHost(item)"
          >
            {{ item }}
          </div>
        </div>
      </div>
      <div class="dropdown-wrapper port-wrapper">
        <input 
          type="number" 
          v-model="port" 
          placeholder="Port"
        />
      </div>
      <button @click="handleProbe" class="btn-probe" :disabled="probing">
        {{ probing ? '...' : 'Probe' }}
      </button>
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
    const showHostDropdown = ref(false)
    const probing = ref(false)
    const discoveredServers = ref([])

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

    const savedHosts = computed(() => {
      return [...new Set(savedServers.value.map(s => s.host))]
    })

    const hideDropdowns = () => {
      showHostDropdown.value = false
    }

    const hideDropdownsDelayed = () => {
      setTimeout(() => {
        showHostDropdown.value = false
      }, 200)
    }

    const toggleHostDropdown = () => {
      showHostDropdown.value = !showHostDropdown.value
    }

    const selectHost = (selectedHost) => {
      host.value = selectedHost
      const server = savedServers.value.find(s => s.host === selectedHost)
      if (server) {
        port.value = server.port
      }
      showHostDropdown.value = false
    }

    const handleConnect = () => {
      if (host.value && port.value) {
        emit('connect', { host: host.value, port: port.value })
      }
    }

    const getLocalIp = () => {
      const ips = []
      const interfaces = navigator.hardwareConcurrency || 4
      // Try to get local IP from saved servers or guess common subnets
      const savedHost = savedServers.value[0]?.host
      if (savedHost && savedHost !== 'localhost') {
        const parts = savedHost.split('.')
        if (parts.length === 4) {
          return parts.slice(0, 3).join('.')
        }
      }
      return null
    }

    const handleProbe = async () => {
      probing.value = true
      discoveredServers.value = []
      showHostDropdown.value = true

      const baseSubnet = getLocalIp()
      if (!baseSubnet) {
        // Fallback: scan common subnets
        for (let subnet = 0; subnet <= 2; subnet++) {
          await scanSubnet(`${baseSubnet || '192.168.1'}`)
          if (discoveredServers.value.length > 0) break
        }
        probing.value = false
        return
      }

      await scanSubnet(baseSubnet)
      probing.value = false
    }

    const scanSubnet = async (subnet) => {
      const promises = []
      const timeout = 500 // ms
      
      for (let i = 1; i <= 254; i++) {
        const ip = `${subnet}.${i}`
        const promise = checkServer(ip, port.value, timeout)
          .then(found => {
            if (found && !discoveredServers.value.includes(ip)) {
              discoveredServers.value.push(ip)
            }
          })
          .catch(() => {})
        promises.push(promise)
      }
      
      // Run in batches to avoid overwhelming the browser
      const batchSize = 50
      for (let i = 0; i < promises.length; i += batchSize) {
        await Promise.all(promises.slice(i, i + batchSize))
      }
    }

    const checkServer = (host, port, timeout) => {
      return new Promise((resolve) => {
        const controller = new AbortController()
        const id = setTimeout(() => {
          controller.abort()
          resolve(false)
        }, timeout)
        
        fetch(`http://${host}:${port}/api/status`, {
          method: 'GET',
          signal: controller.signal,
          mode: 'no-cors'
        })
          .then(() => resolve(true))
          .catch(() => resolve(false))
          .finally(() => clearTimeout(id))
      })
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
      savedHosts,
      showHostDropdown,
      probing,
      discoveredServers,
      handleConnect,
      handleProbe,
      hideDropdowns,
      hideDropdownsDelayed,
      toggleHostDropdown,
      selectHost
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
  overflow: visible;
}

.config-row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  align-items: center;
}

input {
  flex: 1 1 140px;
  min-width: 100px;
  max-width: 180px;
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

.dropdown-wrapper {
  position: relative;
  flex: 1 1 140px;
  min-width: 100px;
  max-width: 180px;
}

.port-wrapper {
  flex: 0 0 90px;
  min-width: 70px;
  max-width: 90px;
}

.dropdown-arrow {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: #888;
  cursor: pointer;
  pointer-events: auto;
  font-size: 10px;
  user-select: none;
}

.dropdown-wrapper input {
  padding-right: 25px;
}

.custom-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: #0f3460;
  border-radius: 4px;
  margin-top: 4px;
  max-height: 200px;
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

.dropdown-item.discovered {
  color: #2ed573;
}

.dropdown-item.discovered::before {
  content: '● ';
  color: #2ed573;
}

.dropdown-item.probing {
  color: #888;
  font-style: italic;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  flex-shrink: 0;
  white-space: nowrap;
}

.btn-probe {
  background: #ffa502;
  color: #1a1a2e;
}

.btn-probe:hover {
  background: #ffbe4d;
}

.btn-probe:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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
