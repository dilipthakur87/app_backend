from datetime import datetime, timezone

from app import db


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, nullable=False)
    reminder_date = db.Column(db.DateTime, nullable=True)
    celery_task_id = db.Column(db.String(50), nullable=True)  # Store Celery task ID
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    def as_dict(self):
        """
        Convert the SQLAlchemy object to a dictionary, excluding non-serializable fields.
        """
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "celery_task_id": self.celery_task_id,
            "reminder_date": self.reminder_date.isoformat() if self.reminder_date else None
        }
