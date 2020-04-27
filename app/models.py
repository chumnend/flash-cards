from hashlib import md5
from datetime import datetime
from flask_login import UserMixin
from app import db, login

# ASSOCIATION TABLES ================================================
followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)

# USER ==============================================================
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    decks = db.relationship('Deck', backref='author', lazy='dynamic')
    cards = db.relationship('Card', backref='author', lazy='dynamic')
    followed = db.relationship(
        'User', 
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
    )

    def __repr__(self):
        return f'<User {self.username}>'

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)


    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter( followers.c.followed_id == user.id ).count() > 0
        
    def followed_decks(self):
        followed = Deck.query.join(
            followers, (
                followers.c.followed_id == Deck.user_id)).filter( 
                    followers.c.follower_id == self.id 
            )
        own = Deck.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Deck.created.desc())
    
    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

# DECK ==============================================================
class Deck(db.Model):
    __tablename__ = 'decks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(140))
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_edited = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    cards = db.relationship('Card', cascade='all', backref='deck', lazy='dynamic')

    def __repr__(self):
        return f'<Deck {self.name}>'


# CARD ==============================================================
class Card(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.String(64))
    back = db.Column(db.String(64))
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    deck_id = db.Column(db.Integer, db.ForeignKey('decks.id'))

    def __repr__(self):
        return f'<Card {self.front}|{self.back}>'
