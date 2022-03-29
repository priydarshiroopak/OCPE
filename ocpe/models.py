from datetime import datetime
from ocpe import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    type = db.Column(db.String(12), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        "polymorphic_on": type
    }

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.type}')"

class Contestant(User):
    __tablename__ = 'contestant'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    rating = db.Column(db.Integer, nullable=False, default=0)
    # submissions = db.relationship('submission', backref='submitter', lazy=True)
    # contests = db.relationship('Contest', backref='contestant', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'contestant'
    }

class Judge(User):
    __tablename__ = 'judge'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    noProblems = db.Column(db.Integer, nullable=False, default=0)
    # contests = db.relationship('judge', backref='author', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'judge'
    }

# class Admin(User):
#     __tablename__ = 'admin'
#     id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

#     __mapper_args__ = {
#         'polymorphic_identity': 'admin'
#     }


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

db.create_all()