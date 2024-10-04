
from app import app, celery, mail
from app.models import Note
from flask_mail import Message

# USER_EMAIL = 'dilip@dilip.com.np'
@celery.task
def remind_note(note_id):
    print(f'message in celery, note_id= {note_id}')
    with app.app_context():
        note = Note.query.get(note_id)
        # Send an email or notification (assuming you have Flask-Mail setup)
        if note:
            body = f"Don't forget: {note.body}"
            print('yo ho hai mero message', body)

            try:
                msg = Message(note.title or 'Test subject' , recipients=['dileepthakur87@gmail.com'])
                msg.body = body
                mail.send(msg)
                return True
            except Exception as e:
                print(f"Error sending email: {e}")
                return False
