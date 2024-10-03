from datetime import datetime

from flask import jsonify, request

from app import app, celery, db
from app.models import Note
from app.tasks import remind_note
from app.utils import validate_datetime


@app.route("/notes", methods=["GET"])
def get_notes():
    notes = Note.query.all()
    return jsonify([note.as_dict() for note in notes])


@app.route("/notes", methods=["POST"])
@validate_datetime("reminder_date")  # Applying the decorator
def create_note():
    data = request.get_json()
    note = Note(
        title=data["title"],
        body=data["body"],
        reminder_date=datetime.strptime(data["reminder_date"], "%Y-%m-%dT%H:%M:%S")
        if data.get("reminder_date")
        else None,
    )
    db.session.add(note)
    db.session.commit()
    if note.reminder_date:
        task_id = schedule_reminder_async(note.id, note.reminder_date)
        note.celery_task_id = task_id

        print('Note created successfully!', 'success')
    
    db.session.commit()
    return jsonify(note.as_dict()), 201


@app.route("/notes/<int:id>", methods=["PUT"])
@validate_datetime("reminder_date")  # Applying the decorator
def update_note(id):
    note = Note.query.get_or_404(id)
    data = request.get_json()

    note.title = data.get("title", note.title)
    note.body = data.get("body", note.body)
    # note.reminder_date = (
    #     datetime.strptime(data["reminder_date"], "%Y-%m-%dT%H:%M:%S")
    #     if data.get("reminder_date")
    #     else None
    # )
    new_reminder_date = datetime.strptime(data["reminder_date"], "%Y-%m-%dT%H:%M:%S")
    if new_reminder_date != note.reminder_date and note.celery_task_id:
            celery.control.revoke(note.celery_task_id,  terminate=True)
    
    note.reminder_date = new_reminder_date
    db.session.commit()
    if new_reminder_date:
        task_id = schedule_reminder_async(note.id, new_reminder_date)
        note.celery_task_id = task_id

    db.session.commit()

    return jsonify(note.as_dict())

def schedule_reminder_async(note_id, new_reminder_date):
    if isinstance(new_reminder_date, str):
        eta = datetime.strptime(new_reminder_date, '%Y-%m-%dT%H:%M:%S')
    else:
        eta = new_reminder_date 
    task = remind_note.apply_async(args=[note_id], eta=eta)
    return task.id


@app.route("/notes/<int:id>", methods=["DELETE"])
def delete_note(id):
    note = Note.query.get_or_404(id)
    if note.celery_task_id:
        celery.control.revoke(note.celery_task_id,  terminate=True)
    db.session.delete(note)
    db.session.commit()
    return "", 204

@app.route("/remind/<int:note_id>", methods=["POST"])
@validate_datetime("reminder_date") 
def set_reminder(note_id):
    data = request.get_json()
    reminder_date=datetime.strptime(data["reminder_date"], "%Y-%m-%dT%H:%M:%S")
    note = Note.query.get_or_404(note_id)
    if reminder_date!= note.reminder_date and note.celery_task_id:
        celery.control.revoke(note.celery_task_id,  terminate=True)
    
    task_id = schedule_reminder_async(note.id, note.reminder_date)
    note.celery_task_id = task_id
    return jsonify({'task_id': note.celery_task_id})
    
    


