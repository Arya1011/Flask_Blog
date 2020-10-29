from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email

users=Blueprint('users',__name__)

@users.route('/register',methods=['POST','GET'])
def register():
	#if already authenticated redirect to home page
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form=RegistrationForm()
	if form.validate_on_submit():
		hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user=User(username=form.username.data,email=form.email.data,password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Account has been created! You can now Log in.','success')
		return redirect(url_for('users.login'))
	return render_template('register.html',title='Register',form=form)

@users.route('/login',methods=['POST','GET'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form=LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		#check for password and if user exists in database
		if user and bcrypt.check_password_hash(user.password,form.password.data):
			login_user(user,remember=form.remember.data)
			#this is the way to get a particular argument from the url
			next_page=request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('main.home'))
		else:
			flash(f'Login unsuccessful,please check email or password','danger')
	return render_template('login.html',title='Login',form=form)

@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.home'))

@users.route('/account',methods=['POST','GET'])
@login_required
def account():
	form=UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			#Returns the filename
			picture_file=save_picture(form.picture.data)
			#updating image file as the compressed image
			current_user.image_file=picture_file
		current_user.username=form.username.data
		current_user.email=form.email.data
		db.session.commit()
		flash('Your account details have been updated',category='success')
		return redirect(url_for('users.account'))
	elif request.method=='GET':
		form.username.data=current_user.username
		form.email.data=current_user.email
	image_file=url_for('static',filename='profile_pics/'+current_user.image_file)
	return render_template('account.html',title='Account',image_file=image_file,form=form)


@users.route('/user/<string:username>')
def user_posts(username):
	#Grabbing all the data from the database
	#Now we can add pagination to get only some of the posts and increase delivery speed of our app
	# posts=Post.query.all()
	page=request.args.get('page',1,type=int)
	#pick a user from the database by filtering accorfing to username
	user=User.query.filter_by(username=username).first_or_404()
	posts=Post.query.filter_by(author=user)\
	.order_by(Post.date_posted.desc())\
	.paginate(page=page,per_page=4)
	return render_template('user_posts.html',posts=posts,user=user)

@users.route('/reset_password',methods=['POST','GET'])
def reset_request():
	#user is logged out beffore they change their password(already logged in doesnt make sense)
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form=RequestResetForm()
	#handling validation of form
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent with instructions to reset your password','info')
		return redirect(url_for('users.login'))
	return render_template('reset_request.html',title='Reset Password',form=form)


@users.route('/reset_password/<token>',methods=['POST','GET'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	#if its a valid token then we get back the user id
	user=User.verify_reset_token(token)
	if user is None:
		flash('That is an invalid or expired token','warning')
		return redirect(url_for('users.reset_request'))
	form=ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password=hashed_password
		db.session.commit()
		flash('Password has been reset! You can now Log in.','success')
		return redirect(url_for('main.login'))
	return render_template('reset_token.html',title='Reset Password',form=form)