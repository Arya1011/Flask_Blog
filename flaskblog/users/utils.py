
import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail


def save_picture(form_picture):
	random_hex=secrets.token_hex(8)
	_ ,f_ext=os.path.splitext(form_picture.filename)
	#Now will encrypt the image name 
	picture_fn=random_hex+f_ext
	#The path of the image file 
	picture_path=os.path.join(current_app.root_path,'static/profile_pics',picture_fn)
	
	#Reshaping the image(use PIL) to save memeory in our file system
	output_size=(125,125)
	#New resolution of the image
	i=Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn

#Sending email to user for resetting password
def send_reset_email(user):
	token=user.get_reset_token()
	msg=Message('Password Reset Request',sender='noreply@demo.com',recipients=[user.email])
	#_external is used to get an absolute URL and not a relative URL
	msg.body=f'''To reset your password,visit the following link:
	{url_for('users.reset_token',token=token,_external=True)}
    If you have not made this request then simply ignore the mail and no changes will be made
	'''
	mail.send(msg)

