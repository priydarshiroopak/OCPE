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
    # posts = db.relationship('Post', backref='author', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        "polymorphic_on": type
    }

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.type}')"

class Submission(db.Model):
    __tablename__='submission'
    contestant_id = db.Column(db.Integer, db.ForeignKey('contestant.id'))
    problem_id = db.Column(db.Integer, db.ForeignKey('problem.id'))
    code=db.Column(db.Integer,db.ForeignKey('code'))
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    cases_passed = db.Column(db.Integer, default=0)

    # submitter = db.relationship('Contestant', backref='submission', lazy=True)
    # problem = db.relationship('Problem', backref='submission', lazy=True)
    
    def __repr__(self):
        return f"Submission( id: '{self.id}', by: '{self.contestant_id}', for: '{self.problem_id}', cases passed: '{self.cases_passed}')"

class Contestant(User):
    __tablename__ = 'contestant'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    rating = db.Column(db.Integer, nullable=False, default=0)

    submissions = db.relationship('Submission', backref='author', lazy=True)
    # contests = db.relationship('Contest', backref='contestant', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'contestant'
    }

    def __repr__(self):
        return f"Contestant( id: '{self.id}', name: '{self.username}', email: ' {self.email}', rating: '{self.rating}', submissions: '{self.submissions}')"

class Judge(User):
    __tablename__ = 'judge'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    noProblems = db.Column(db.Integer, nullable=False, default=0)
    # contests = db.relationship('judge', backref='author', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'judge'
    }

    def __repr__(self):
        return f"Judge( id: '{self.id}', name: '{self.username}', email: ' {self.email}', number of problems: '{self.noProblems}')"

# class Admin(User):
#     __tablename__ = 'admin'
#     id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

#     __mapper_args__ = {
#         'polymorphic_identity': 'admin'
#     }

class Problem(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    title = db.Column(db.String(120), nullable=False, default='Problem {}'.format(id))
    desc = db.Column(db.Text, nullable=False, default='No description added!')
    
    submissions = db.relationship('Submission', backref='author', lazy=True)

    def __repr__(self):
        return f"Problem( id: '{self.id}', title: '{self.title}', desc: ' {self.desc}', submissions: '{self.submissions}')"

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     content = db.Column(db.Text, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#     def __repr__(self):
#         return f"Post('{self.title}', '{self.date_posted}')"

db.create_all()
