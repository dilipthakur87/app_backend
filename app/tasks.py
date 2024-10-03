
from app import app, celery
from app.models import Note

USER_EMAIL = 'dilip@dilip.com.np'
@celery.task
def remind_note(note_id):
    print(f'message in celery, note_id= {note_id}')
    with app.app_context():
        note = Note.query.get(note_id)
        # Send an email or notification (assuming you have Flask-Mail setup)
        if note:
            # msg = Message('Reminder: ' + note.title,
            #             sender='noreply@demo.com',
            #             recipients=[USER_EMAIL])
            body = f"Don't forget: {note.title}"
            print('yo ho hai mero message', body)
            # mail.send(msg)