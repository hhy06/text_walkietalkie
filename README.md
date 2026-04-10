# Text Walkie Talkie

A walkie talkie style program for sharing text messages within a LAN.

## Quick Start

```bash
./start.sh
```

Or manually:

### 1. Start the Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The backend server will run on `http://0.0.0.0:12358` (accessible from any machine in the LAN).

### 2. Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend dev server will run on `http://localhost:3000`.

## Accessing from Other Machines

On any device connected to the same network:

1. Find the host machine's IP address (e.g., `192.168.1.100`)
2. Open the browser on that machine and go to `http://localhost:3000`
3. Enter the backend server address (e.g., `192.168.1.100:12358`) in the connection panel

### Finding Your IP Address

**Linux/Mac:**
```bash
ip addr show | grep "inet "     # Linux
ifconfig | grep "inet "         # macOS
```

**Windows:**
```bash
ipconfig
```
Look for IPv4 Address under your active network adapter.

## Network Requirements

- All devices must be on the same local network (WLAN/LAN)
- Ensure firewall allows connections on ports 3000 and 12358
- CORS is enabled on the backend for cross-origin requests

## Building for Production

```bash
cd frontend
npm run build
```

The production build will be in `frontend/dist/`.

## Troubleshooting

### Frontend won't start (Userland/WSL environments)
If Vite fails with `uv_interface_addresses` errors, the dev server will run on localhost only. Access it from the same machine using `http://localhost:3000`. The backend will still be accessible from other machines on the network.
