from flask import render_template, url_for, flash, redirect, request
from ocpe import app, db, bcrypt
from ocpe.forms import SignupForm, LoginForm
from ocpe.models import Contestant, User, Post, Judge
from flask_login import login_user, current_user, logout_user, login_required
from ocpe.forms import SignupForm

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html', posts=posts)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        type = form.type.data
        if type == 'judge':
            user = Judge(username=form.username.data, email=form.email.data, password=hashed_password, type=type)
        else:
            user = Contestant(username=form.username.data, email=form.email.data, password=hashed_password, type=type)
        # user = User(username=form.username.data, email=form.email.data, password=hashed_password, type=type)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Signup', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')

@app.route("/contests")
def contests():
    return render_template('contests.html', title='Contests')

@app.route("/contest")
def contest():
    return render_template('contest.html', title='Contest #')

@app.route("/problems")
def problems():
    return render_template('problems.html', title='Problems')

@app.route("/question")
def question():
    return render_template('question.html', title='Question#')

@app.route("/404")
def wrongDirect():
    return render_template('404.html', title='404', wrongDirect=True)