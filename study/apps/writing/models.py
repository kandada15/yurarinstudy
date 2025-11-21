from apps.app import db
from sqlalchemy import ForeignKey

class WritingProgress(db.Model):
    __tablename__ = 'progress'
    progress_id = db.Column(db.String(10), primary_key=True, nullable=False)
    step_id = db.Column(db.String(10), db.ForeignKey('steps.step_id'), nullable=False)
    student_id = db.Column(db.String(10), db.ForeignKey('students.student_id'), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)

class Step(db.Model):
    __tablename__ = 'steps'
    step_id = db.Column(db.String(10), primary_key=True, nullable=False)
    step_name = db.Column(db.String(20), nullable=False)
    text_name = db.Column(db.String(30), nullable=False)
    text_content = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.String(10), db.ForeignKey('categories.category_id'), nullable=False)

class Category(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(db.String(10), primary_key=True, nullable=False)
    category_name = db.Column(db.String(20), nullable=False)