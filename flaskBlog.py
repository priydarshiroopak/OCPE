from flask import Flask, render_template, url_for, flash, redirect
from forms import SignupForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

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
    form = SignupForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('signup.html', title='Signup', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


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

if __name__ == '__main__':
    app.run(debug=True)