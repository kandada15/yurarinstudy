from apps.app import db
from sqlalchemy import ForeignKey
from datetime import datetime

class Task_Base(db.Model):
    __tablename__ = 'task'
    task_id = db.Column(db.String(10), primary_key=True, nullable=False)
    task_name = db.Column(db.String(40), nullable=False)
    task_text = db.Column(db.Text, nullable=False)
  
class Task_Send(db.Model):
    __tablename__ = 'task_send'
    task_send_id = db.Column(db.String(10), primary_key=True, nullable=False)
    task_send_limit = db.Column(db.Date, nullable=False)
    task_id = db.Column(db.String(10), db.ForeignKey('task.task_id'), nullable=False)
    student_id = db.Column(db.String(10), db.ForeignKey('student.student_id'), nullable=False)

class Task_Return(db.Model):
    __tablename__ = 'task_return'
    task_return_id = db.Column(db.String(10), primary_key=True, nullable=False)
    check_text = db.Column(db.Text, nullable=False)
    question_answer_text = db.Column(db.Text)
    task_send_id = db.Column(db.String(10), db.ForeignKey('task_send.task_send_id'), nullable=False)

class Task_submission(db.Model):
    __tablename__ = 'task_submission'
    task_sub_id = db.Column(db.String(10), primary_key=True, nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    question_text = db.Column(db.Text)
    task_sub_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    is_sended = db.Column(db.Boolean, default=False)
    is_checked = db.Column(db.Boolean, default=False)
    is_returned = db.Column(db.Boolean, default=False)
    task_id = db.Column(db.String(10), db.ForeignKey('task.task_id'), nullable=False)
    student_id = db.Column(db.String(10), db.ForeignKey('student.student_id'), nullable=False)
    