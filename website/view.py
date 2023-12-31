# store main url endpoints for frontend
# store all routes where the users can go through
from flask import Blueprint, render_template,flash,request
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
views = Blueprint('views',__name__)

#whenever we go to / with our website, we go to home
@views.route('/',methods=['GET','POST'])
@login_required
def home():
	if request.method == 'POST':
		note = request.form.get('note')

		if len(note) == 0:
			flash('Note is too Short', category='error')
		else:
			new_note = Note(data=note,user_id=current_user.id)
			db.session.add(new_note)
			db.session.commit()
			flash('New Note Added', category='success')

	# it will return and display test in h1 tag in frontend
	return render_template("home.html", user=current_user)

@views.route('/delete-note',methods=['POST'])
def delete_note():
	note = json.loads(request.data)
	noteid = note['noteid']
	note = Note.query.get(noteid)
	if note:
		if note.user_id == current_user.id:
			db.session.delete(note)
			db.session.commit()
			return jsonify({})