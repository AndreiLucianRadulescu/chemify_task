from enum import Enum
from flask_login import UserMixin
from app import db
from sqlalchemy.orm import relationship, Mapped

class TaskStatus(Enum):
    PENDING = 0
    DOING = 1
    BLOCKED = 2
    DONE = 3


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Enum(TaskStatus), default=TaskStatus.PENDING)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    hashed_password = db.Column(db.String(25))

    tasks : Mapped["Task"] = db.relationship(
        'Task', back_populates='user_id', lazy=True
    )