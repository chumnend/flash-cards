from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import User, Deck
from config import TestConfig

class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?d=identicon&s=128'))

    def test_follow(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])
    
        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'susan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'john')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_decks(self):
        # create four users
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        u3 = User(username='mary', email='mary@example.com')
        u4 = User(username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four decks
        now = datetime.utcnow()
        d1 = Deck(name="john made this", author=u1, created=now + timedelta(seconds=1))
        d2 = Deck(name="susan made this", author=u2,created=now + timedelta(seconds=4))
        d3 = Deck(name="mary made this", author=u3, created=now + timedelta(seconds=3))
        d4 = Deck(name="david made this", author=u4,created=now + timedelta(seconds=2))
        db.session.add_all([d1, d2, d3, d4])
        db.session.commit()

        # setup the followers
        u1.follow(u2)  # john follows susan
        u1.follow(u4)  # john follows david
        u2.follow(u3)  # susan follows mary
        u3.follow(u4)  # mary follows david
        db.session.commit()

        # check the followed posts of each user
        f1 = u1.followed_decks().all()
        f2 = u2.followed_decks().all()
        f3 = u3.followed_decks().all()
        f4 = u4.followed_decks().all()
        self.assertEqual(f1, [d2, d4, d1])
        self.assertEqual(f2, [d2, d3])
        self.assertEqual(f3, [d3, d4])
        self.assertEqual(f4, [d4])

if __name__ == '__main__':
    unittest.main()
