import sqlite3
from datetime import datetime, timedelta
from typing import List, Optional
from contextlib import contextmanager

from models import Message


class Database:
    def __init__(self, db_path: str = 'walkietalkie.db'):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    @contextmanager
    def _cursor(self):
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            yield cursor
            conn.commit()
        finally:
            conn.close()

    def _init_db(self):
        with self._cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

    def add_message(self, username: str, content: str) -> Message:
        timestamp = datetime.now()
        with self._cursor() as cursor:
            cursor.execute(
                'INSERT INTO messages (username, content, timestamp) VALUES (?, ?, ?)',
                (username, content, timestamp)
            )
            msg_id = cursor.lastrowid
        return Message(id=msg_id, username=username, content=content, timestamp=timestamp)

    def get_messages(self, limit: int = 100, hours: Optional[int] = None) -> List[Message]:
        if hours is not None:
            cutoff = datetime.now() - timedelta(hours=hours)
            query = '''
                SELECT id, username, content, timestamp 
                FROM messages 
                WHERE timestamp >= ? 
                ORDER BY timestamp DESC
            '''
            params = (cutoff,)
        else:
            query = '''
                SELECT id, username, content, timestamp 
                FROM messages 
                ORDER BY timestamp DESC 
                LIMIT ?
            '''
            params = (limit,)

        with self._cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
        
        messages = [Message.from_row(row) for row in rows]
        messages.reverse()
        return messages

    def get_message_count(self) -> int:
        with self._cursor() as cursor:
            cursor.execute('SELECT COUNT(*) FROM messages')
            return cursor.fetchone()[0]
