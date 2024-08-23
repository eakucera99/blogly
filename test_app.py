import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, db, Users

class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home(self):
        with app.app_context():
            response = self.app.get('/')
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, '/users')

    def test_list_users(self):
        with app.app_context():
            user = Users(first_name='John', last_name='Doe', image_url='example.jpg')
            db.session.add(user)
            db.session.commit()

            response = self.app.get('/users')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'John Doe', response.data)

    def test_add_user(self):
        with app.app_context():
            data = {
                'first_name': 'Jane',
                'last_name': 'Smith',
                'image_url': 'example.jpg'
            }

            response = self.app.post('/users/add_user', data=data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Jane Smith', response.data)

    def test_show_user(self):
        with app.app_context():
            user = Users(first_name='John', last_name='Doe', image_url='example.jpg')
            db.session.add(user)
            db.session.commit()

            response = self.app.get(f'/users/{user.id}')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'John Doe', response.data)

    def test_edit_user(self):
        with app.app_context():
            user = Users(first_name='John', last_name='Doe', image_url='example.jpg')
            db.session.add(user)
            db.session.commit()

            data = {
                'first_name': 'Jane',
                'last_name': 'Smith',
                'image_url': 'example.jpg'
            }

            response = self.app.post(f'/users/{user.id}/edit', data=data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Jane Smith', response.data)

    def test_delete_user(self):
        with app.app_context():
            user = Users(first_name='John', last_name='Doe', image_url='example.jpg')
            db.session.add(user)
            db.session.commit()

            response = self.app.post(f'/users/{user.id}/delete', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(b'John Doe', response.data)

if __name__ == '__main__':
    unittest.main()