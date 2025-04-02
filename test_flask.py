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

# if __name__ == '__main__':
#     unittest.main()




###########################

# import unittest
# from app import app
# from unittest import TestCase
# from models import db, User


# # Use test database and don't clutter tests with SQL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
# app.config['SQLALCHEMY_ECHO'] = False

# # Make Flask errors be real errors, rather than HTML pages with error info
# app.config['TESTING'] = True

# # This is a bit of hack, but don't use Flask DebugToolbar
# app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# db.drop_all()
# db.create_all()


# class UserTestCase(TestCase):
#     """Tests for Users."""
# def setUp(self):
#     """clear the table contents and add user"""
#     with app.app_context():
#             User.query.delete()
#             db.session.commit()
#             user = User(first_name="John", last_name="Doe")
#             db.session.add(user)
#             db.session.commit()
#     self.app = app.test_client()
#     self.app.testing = True

# def tearDown(self):
#     """clear up all transactions"""
#     with app.app_context():
#             db.session.rollback()

# def test_showUsers(self):
#     with app.test_client() as client:
#             res = client.get('/')
#             html = res.get_data(as_text=True)

#     self.assertEqual(res.status_code, 302)

# def test_addUser(self):
#     with app.test_client() as client:
#         res = client.get('/users/new')
#         html = res.get_data(as_text=True)

#     self.assertEqual(res.status_code, 200)

# def test_editUser(self):
#     with app.test_client() as client:
#         res = client.get('/users/1/edit')
#         html = res.get_data(as_text=True)

#     self.assertEqual(res.status_code, 200)

# def test_deleteUser(self):
#     with app.test_client() as client:
#         res = client.get('/users/1/delete')
#         html = res.get_data(as_text=True)

#     self.assertEqual(res.status_code, 302)
    

##################


    # def setUp(self):
    #     """Add sample user."""

    #     User.query.delete()

    #     pet = Pet(name="TestPet", species="dog", hunger=10)
    #     db.session.add(pet)
    #     db.session.commit()

    #     self.pet_id = pet.id
    #     self.pet = pet

    # def tearDown(self):
    #     """Clear all transactions."""

    #     db.session.rollback()

    # def test_list_pets(self):
    #     with app.test_client() as client:
    #         resp = client.get("/")
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn('TestPet', html)

    # def test_show_pet(self):
    #     with app.test_client() as client:
    #         resp = client.get(f"/{self.pet_id}")
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn('<h1>TestPet Details</h1>', html)
    #         self.assertIn(self.pet.species, html)

    # def test_add_pet(self):
    #     with app.test_client() as client:
    #         d = {"name": "TestPet2", "species": "cat", "hunger": 20}
    #         resp = client.post("/", data=d, follow_redirects=True)
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn("<h1>TestPet2 Details</h1>", html)

