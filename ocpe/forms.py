from email.policy import default
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from ocpe.models import Problem, User


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    type = RadioField('User type: ', choices=[('contestant','Contestant'),('judge','Judge')], validators=[DataRequired()], default='contestant')
    # print (type.raw_data)
    # type = RadioField('User type: ', choices=[('C','Contestant'),('J','Judge'),('A','Admin')], validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
    
class SubmissionForm(FlaskForm):
    code = StringField('Code')
    submit = SubmitField('Submit Code')  
   
class PostProblemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    #only single test case
    testInput = TextAreaField('Test Case')
    testOutput = TextAreaField('Expected Output',validators=[DataRequired()])
    score = StringField('Score',validators=[DataRequired()], default=100)
    submit = SubmitField('Create Problem')
    
    def validate_name(self, name):
        problem = Problem.query.filter_by(name=name.data).first()
        if problem:
            raise ValidationError('This name is taken. Please choose a different one.')


