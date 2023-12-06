import unittest
from flask import Flask
from flask_testing import TestCase
from your_app import create_app, db

class TestApp(TestCase):
    def create_app(self):
        app = create_app('config_test.py')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_registration(self):
        response = self.client.post('/register', data=dict(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            confirm_password='testpassword'
        ), follow_redirects=True)
        self.assert200(response)
        self.assertIn(b'You have registered successfully', response.data)

    def test_article_creation(self):
        self.client.post('/register', data=dict(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            confirm_password='testpassword'
        ), follow_redirects=True)
        response = self.client.post('/create_article', data=dict(
            title='Test Article',
            content='This is a test article',
        ), follow_redirects=True)
        self.assert200(response)
        self.assertIn(b'Article created successfully', response.data)

if __name__ == '__main__':
    unittest.main()
