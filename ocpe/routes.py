from flask import render_template, url_for, flash, redirect, request
from ocpe import app, db, bcrypt
from ocpe.forms import SignupForm, LoginForm
from ocpe.models import User, Post
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
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
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
    
@app.route("/IDE")
def submit():
	if request.method=='POST':

		#Getting input(code and input for program) and checkbox value from the form.
		code=request.form['code']
		inp=request.form['input']
		chk=request.form.get('check')

		#Checking if the checkbox is checked or not.
		if  not chk=='1':
			#If checkbox was not ckecked then the input field will be empty and checkbox will be unchecked. 
			inp=""
			check=''
		else:
			##If checkbox was ckecked then the input field will stay the same and checkbox will be checked.
			check='checked'	

		#calling the function to compile and execute the c program.	
		output=complier_output(code,inp,chk)
	#return render_tempelate to 	
	return render_template('home.html',code=code,input=inp,output=output,check=check)

def complier_output(code,inp,chk):
	#checking if a file already exists or not in no the create one.
	if not os.path.exists('Try.c'):
		os.open('Try.c',os.O_CREAT)
	#creating a file descriptor to write in to the file.	
	fd=os.open("Try.c",os.O_WRONLY)
	#truncate the content of the file to 0 bytes so that there is no overwriting in any way using the write operation.
	os.truncate(fd,0)
	#encode the string into bytes.
	fileadd=str.encode(code)
	#write to the file.
	os.write(fd,fileadd)
	#close the file descriptor.
	os.close(fd)
	#Compiling the c program file and retrieving the error if any. 
	s=subprocess.run(['gcc','-o','new','Try.c'],stderr=PIPE,)
	#storing the value returned by return code.
	check=s.returncode
	#checking whether program compiled succesfully or not.
	if check==0:
		#cheking whether input for program is enabled or not.
		if chk=='1':
			#executing the program with input.
			r=subprocess.run(["./new"],input=inp.encode(),stdout=PIPE)
		else:
			#executing the program without input.
			r=subprocess.run(["./new"],stdout=PIPE)
		#return the output of the program.	
		return r.stdout.decode("utf-8")
	else:
		#return the error if the program did not compile successfully
		return s.stderr.decode("utf-8")

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'),404
