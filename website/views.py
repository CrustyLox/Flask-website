from flask import Blueprint,render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views',__name__)

@views.route('/',methods =['POST', 'GET'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('note is too short',category='error')
        else:
            new_note = Note(data=note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('note uploaded succesfully',category='success')
    return render_template("home.html", user = current_user)

@views.route('/delete-node',methods=['POST'])
def delete_node():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({})
        