import unittest
from app import app, db, User

class UserViewsTestCase(unittest.TestCase):
    """Tests for user-related routes."""

    @classmethod
    def setUpClass(cls):
        """Set up test database before running tests."""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
        app.config['TESTING'] = True
        cls.client = app.test_client()
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Clean up test database after tests."""
        with app.app_context():
            db.drop_all()

    def setUp(self):
        """Set up sample data."""
        with app.app_context():
            User.query.delete()
            user = User(first_name='John', last_name='Doe', image_url='')
            db.session.add(user)
            db.session.commit()
            self.user_id = user.id

    def tearDown(self):
        """Clean up database after each test."""
        with app.app_context():
            db.session.rollback()

    def test_users_index(self):
        """Test the users index route."""
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John Doe', response.data)

    def test_users_new_form(self):
        """Test showing the new user form."""
        response = self.client.get('/users/new')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create a user', response.data)

    def test_users_show(self):
        """Test showing a specific user page."""
        response = self.client.get(f'/users/{self.user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John Doe', response.data)

    def test_users_delete(self):
        """Test deleting a user."""
        response = self.client.post(f'/users/{self.user_id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'John Doe', response.data)


