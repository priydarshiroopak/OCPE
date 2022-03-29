from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from ocpe.models import User


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    type = RadioField('User type: ', choices=[('contestant','Contestant'),('judge','Judge')], validators=[DataRequired()])
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
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    #only single test case
    testcase=TextAreaField('Test Case',validators=[DataRequired()])
    expected_output=TextAreaField('Sample Output',validators=[DataRequired()])
    score=TextAreaField('Score',validators=[DataRequired()])
    submit = SubmitField('Post')

