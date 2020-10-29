from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User

class RegistrationForm(FlaskForm):
	username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
	email=StringField('Email',validators=[DataRequired(),Email()])
	password=PasswordField('Password',validators=[DataRequired()])
	confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
	submit=SubmitField('Sign Up')

    #These functions will help prevent repetition of username and email
	def validate_username(self,username):
		#We are trying to search our db for this user
		user=User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username is taken!')

	def validate_email(self,email):
		#We are trying to search our db for this user
		user=User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email is already registered!')

class LoginForm(FlaskForm):
	email=StringField('Email',validators=[DataRequired(),Email()])
	password=PasswordField('Password',validators=[DataRequired()])
	remember=BooleanField('Remember Me')
	submit=SubmitField('Login')




class UpdateAccountForm(FlaskForm):
	username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
	email=StringField('Email',validators=[DataRequired(),Email()])
	picture=FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png'])])
	submit=SubmitField('Update')
    
	def validate_username(self,username):
		#We are trying to search our db for this user
		if username.data!=current_user.username:
			user=User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('Username is taken!')
		

	def validate_email(self,email):
		#We are trying to search our db for this user
		if email.data!=current_user.email:
			user=User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('Email is already registered!')


class RequestResetForm(FlaskForm):
	email=StringField('Email',validators=[DataRequired(),Email()])
	submit=SubmitField('Request Password Reset')
	def validate_email(self,email):
		#We are trying to search our db for this user
		user=User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('Email is not registered,please register first.')

class ResetPasswordForm(FlaskForm):
	password=PasswordField('Password',validators=[DataRequired()])
	confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
	submit=SubmitField('Reset Password')