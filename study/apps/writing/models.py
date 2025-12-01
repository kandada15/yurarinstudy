from apps.app import db
from sqlalchemy import ForeignKey

class Category(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(db.Integer(10), primary_key=True, nullable=False)
    category_name = db.Column(db.String(20), nullable=False)

class Stage(db.Model):
    __tablename__ = 'stage'
    stage_id = db.Column(db.Integer(10), primary_key=True, nullable=False)
    stage_name = db.Column(db.String(5), nullable=False)
    category_id = db.Column(db.Integer(10), db.ForeignKey('categories.category_id'), nullable=False)


class Step(db.Model):
    __tablename__ = 'steps'
    step_id = db.Column(db.Integer(10), primary_key=True, nullable=False)
    step_name = db.Column(db.String(50), nullable=False)
    stage_id = db.Column(db.Integer(10), db.ForeignKey('stage.stage_id'), nullable=False)

    # text_name = db.Column(db.String(30), nullable=False)
    # text_content = db.Column(db.Text, nullable=False)
    # category_id = db.Column(db.String(10), db.ForeignKey('categories.category_id'), nullable=False)

class Text(db.Model):
    __tablename__ = 'text'
    text_id = db.Column(db.Integer(10), primary_key=True, nullable=False)
    text_content = db.Column(db.Text, nullable=False)
    text_answer = db.Column(db.Text)
    step_id = db.Column(db.Integer(10), db.ForeignKey('steps.step_id'), nullable=False)

class WritingProgress(db.Model):
    __tablename__ = 'progress'
    progress_id = db.Column(db.Integer(10), primary_key=True, nullable=False)
    is_step_completed = db.Column(db.Boolean, default=False)
    step_id = db.Column(db.Integer(10), db.ForeignKey('steps.step_id'), nullable=False)
    student_id = db.Column(db.Integer(10), db.ForeignKey('students.student_id'), nullable=False)