from enum import Enum
from flask_login import UserMixin
from app import db, login
from sqlalchemy.orm import relationship, Mapped
from werkzeug.security import check_password_hash
from sqlalchemy import DateTime, func

class TaskStatus(Enum):
    PENDING = 0
    DOING = 1
    BLOCKED = 2
    DONE = 3


user_task_table = db.Table(
    "user_task_table",
    db.Model.metadata,
    db.Column("user_id", db.ForeignKey("user.id"), primary_key=True),
    db.Column("task_id", db.ForeignKey("task.id"), primary_key=True)
)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Enum(TaskStatus), default=TaskStatus.PENDING)
    user_id : Mapped["User"] = db.relationship(
        'User', back_populates='tasks', secondary=user_task_table, uselist=False
    )

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    hashed_password = db.Column(db.String(128))

    tasks : Mapped["Task"] = db.relationship(
        'Task', back_populates='user_id', lazy=True, secondary=user_task_table
    )

    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
    

class TaskHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deleted_at = db.Column(db.DateTime, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    task_id = db.Column(db.Integer, nullable=False)