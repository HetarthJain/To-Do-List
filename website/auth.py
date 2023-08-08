from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth',__name__)
@auth.route('/login',methods=['GET','POST'])
def login():
	if request.method == 'POST':
		email = request.form.get('email')
		password = request.form.get('password1')
		password = password.encode("utf-8") 
		

		#check if user email exists in db
		user = User.query.filter_by(email=email).first()
		if user: 
			if check_password_hash(user.password, password.decode("utf-8")):
				flash('Logged in successfully!', category='success')
				login_user(user, remember=True)
				return redirect(url_for('views.home'))
			else:
				flash('Incorrect password, try again.', category='error')
		else:
			flash('Email does not exist.', category='error')
	return render_template("login.html",user = current_user)

@auth.route('/logout')
@login_required
def logout():
	return render_template("auth.login")

@auth.route('/signup',methods=['GET','POST'])
def sign_up():
	if request.method == 'POST':
		email = request.form.get('email')
		firstname = request.form.get('firstname')
		password1 = request.form.get('password1')
		password2 = request.form.get('password2')

		user = User.query.filter_by(email=email).first()
		if user:
			flash('Email already Exists',category='error')
		elif len(email)<4:
			flash('Email must be longer than 4 characters',category='error')
		elif len(firstname)<2:
			flash('Name must be longer than 2 characters',category='error')
		elif password1!=password2:
			flash('Password do not Match',category='error')
		elif len(password1)<7:
			flash('Password must be longer than 7 characters',category='error')
		else:
			#add user to db
			new_user = User(email = email,name = firstname, password = generate_password_hash(password1,method='sha256'))
			db.session.add(new_user) 
			db.session.commit()
			flash('Account Created!',category='success')
			return redirect(url_for('views.home'))

	return render_template("signup.html",user=current_user)