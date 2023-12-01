from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):

        app.config['TESTING'] = True
        self.client = app.test_client()
        # This is used to simulate requests without running in a web server

    def test_show_board(self):
        """Test if the board template is rendered and session is set"""
        with self.client as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn('board', session)

    def test_check_word(self):
        """Test if the word is valid"""
        with self.client as client:
            test_board = [['T', 'E', 'S', 'T'],
                          ['T', 'E', 'S', 'T'],
                          ['T', 'E', 'S', 'T'],
                          ['T', 'E', 'S', 'T'],
                          ['T', 'E', 'S', 'T']]
            with client.session_transaction() as sess:
                sess['board'] = test_board

            response = client.get('/check-word?guess=test')
            self.assertEqual(response.status_code, 200)
            json_data = response.get_json()
            self.assertEqual(json_data['result'], 'ok')

    def test_update_stats(self):
        """Test if player stats get updated"""
        with self.client as client:
            response = client.post('/update-stats', json = {'score': 10, 'highScore': 20, 'playCount': 2})
            self.assertEqual(response.status_code, 200)
            json_data = response.get_json()
            self.assertEqual(json_data['status'], 'success')
            self.assertEqual(json_data['message'], 'Stats updated')

