import unittest
import json
import os
import sys
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import database
import tempfile
import os

temp_db_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
temp_db_file.close()
db_instance = database.Database(temp_db_file.name)

import app
app.db = db_instance


class TestBackend(unittest.TestCase):
    def setUp(self):
        self.app = app.app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def tearDown(self):
        conn = app.db._get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM messages')
        conn.commit()
        conn.close()

    def test_status_endpoint(self):
        response = self.client.get('/api/status')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'online')
        self.assertIn('message_count', data)

    def test_get_messages_empty(self):
        response = self.client.get('/api/messages')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['messages'], [])

    def test_post_message(self):
        payload = {
            'username': 'TestUser',
            'content': 'Hello, this is a test message!'
        }
        response = self.client.post(
            '/api/messages',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        
        data = json.loads(response.data)
        self.assertEqual(data['username'], 'TestUser')
        self.assertEqual(data['content'], 'Hello, this is a test message!')
        self.assertIn('id', data)
        self.assertIn('timestamp', data)

    def test_post_message_missing_username(self):
        payload = {'content': 'Hello'}
        response = self.client.post(
            '/api/messages',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_post_message_missing_content(self):
        payload = {'username': 'TestUser'}
        response = self.client.post(
            '/api/messages',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_post_message_empty_content(self):
        payload = {'username': 'TestUser', 'content': '   '}
        response = self.client.post(
            '/api/messages',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_get_messages_after_post(self):
        payload = {'username': 'User1', 'content': 'First message'}
        self.client.post(
            '/api/messages',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        payload = {'username': 'User2', 'content': 'Second message'}
        self.client.post(
            '/api/messages',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        response = self.client.get('/api/messages')
        data = json.loads(response.data)
        
        self.assertEqual(len(data['messages']), 2)
        self.assertEqual(data['messages'][0]['content'], 'First message')
        self.assertEqual(data['messages'][1]['content'], 'Second message')

    def test_get_messages_with_limit(self):
        for i in range(5):
            self.client.post(
                '/api/messages',
                data=json.dumps({'username': 'User', 'content': f'Message {i}'}),
                content_type='application/json'
            )
        
        response = self.client.get('/api/messages?limit=3')
        data = json.loads(response.data)
        
        self.assertEqual(len(data['messages']), 3)

    def test_multiple_users(self):
        users = ['Alice', 'Bob', 'Charlie']
        for user in users:
            self.client.post(
                '/api/messages',
                data=json.dumps({'username': user, 'content': f'Hello from {user}'}),
                content_type='application/json'
            )
        
        response = self.client.get('/api/messages')
        data = json.loads(response.data)
        
        usernames = [msg['username'] for msg in data['messages']]
        for user in users:
            self.assertIn(user, usernames)


class MockFrontendClient:
    def __init__(self, base_url='http://localhost:12358'):
        self.base_url = base_url

    def connect(self, host, port):
        self.base_url = f'http://{host}:{port}'

    def send_message(self, username, content):
        import requests
        response = requests.post(
            f'{self.base_url}/api/messages',
            json={'username': username, 'content': content}
        )
        return response

    def get_messages(self, limit=100):
        import requests
        response = requests.get(f'{self.base_url}/api/messages?limit={limit}')
        return response

    def get_status(self):
        import requests
        response = requests.get(f'{self.base_url}/api/status')
        return response


if __name__ == '__main__':
    unittest.main()
