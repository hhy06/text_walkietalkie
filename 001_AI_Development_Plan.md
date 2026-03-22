# 001 AI Development Plan: Text Walkie Talkie

## Project Overview
A walkie talkie style program that shares text information within a WLAN (Local Area Network).

## User Experience

### Connection Flow
1. User accesses the web page frontend
2. User enters server IP and port (or selects from saved history)
3. Server connection status is displayed
4. Saved connection info persists in local storage/cookies

### Message Display
1. Server shows all connected users
2. Displays most recent 100 messages OR all messages from past 12 hours (configurable)
3. Real-time message updates via polling or WebSocket

### Message Entry
1. User types message in input box
2. Presses send to transmit
3. Messages appear in dialogue with sender identification

## Tech Stack

### Backend
- **Language**: Python
- **Framework**: Flask
- **Database**: SQLite
- **Storage**: All messages persisted with timestamps

### Frontend
- **Framework**: Vue.js
- **Styling**: CSS (simple, clean UI)
- **State**: Local storage for server history

## Architecture

### Backend API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/messages` | Retrieve messages (with optional limit/time filter) |
| POST | `/api/messages` | Send a new message |
| GET | `/api/status` | Check server status |
| GET | `/api/users` | List connected users |

### Database Schema

**messages table**:
- id (INTEGER PRIMARY KEY)
- username (TEXT)
- content (TEXT)
- timestamp (DATETIME)

### Frontend Components

1. **ConnectionPanel**: Server IP/port input, connect button, status indicator
2. **MessageDialogue**: Scrollable message list with sender and content
3. **MessageInput**: Text input and send button

## File Structure

```
text_walkietalkie/
├── backend/
│   ├── app.py              # Flask application
│   ├── database.py         # Database operations
│   ├── models.py           # Data models
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── index.html          # Entry point
│   ├── src/
│   │   ├── App.vue         # Main component
│   │   ├── components/
│   │   │   ├── ConnectionPanel.vue
│   │   │   ├── MessageDialogue.vue
│   │   │   └── MessageInput.vue
│   │   └── main.js         # Vue entry
│   └── package.json
└── tests/
    └── test_backend.py     # Backend test suite
```

## Development Steps

### Step 1: Backend Development
1. Set up Flask application structure
2. Create SQLite database schema
3. Implement message CRUD operations
4. Add CORS support for frontend access
5. Write automated tests

### Step 2: Frontend Development
1. Set up Vue project
2. Create ConnectionPanel component
3. Create MessageDialogue component
4. Create MessageInput component
5. Implement API communication
6. Add local storage for server history

## Configuration Options

### Message Retention
- Default: Last 100 messages
- Option: Last 12 hours of messages
- Configurable via frontend dropdown

### Server Settings (Backend)
- Default port: 5000
- Host: 0.0.0.0 (bind to all interfaces for LAN access)

### Frontend Network Settings
- Dev server port: 3000
- Host: 0.0.0.0 (accessible from any machine in the LAN)
- To run on a different port: `npm run dev -- --port <PORT>`

