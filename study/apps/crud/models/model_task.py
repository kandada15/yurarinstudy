from apps.extensions import db
from datetime import datetime

class TaskStreamed(db.Model):
    __tablename__ = 'task_streamed'

    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_name = db.Column(db.String(255), nullable=False)
    streamed_date = db.Column(db.DateTime, default=datetime.now)
    due_date = db.Column(db.DateTime)
    
    # 管理者IDとの紐付け
    admin_id = db.Column(db.String(10), db.ForeignKey('admin.admin_id'))
    
    # 管理者モデルとのリレーション
    admin = db.relationship('Admin', backref='streamed_tasks')