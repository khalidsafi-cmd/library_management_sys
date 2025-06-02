import unittest
from app import create_app, db
from app.models import User, Book

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            user = User(username="testuser", email="test@example.com")
            user.set_password("testpass")
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_user_creation(self):
        with self.app.app_context():
            user = User.query.filter_by(username="testuser").first()
            self.assertIsNotNone(user)
            self.assertTrue(user.check_password("testpass"))

    def test_book_addition(self):
        with self.app.app_context():
            book = Book(title="Test Book", author="Author", year=2024, language="English")
            db.session.add(book)
            db.session.commit()
            self.assertEqual(Book.query.count(), 1)

if __name__ == '__main__':
    unittest.main()
