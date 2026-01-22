from apps.extensions import db
from datetime import datetime

# Student テーブルモデル作成
class Student(db.Model):
    __tablename__ = 'student'
    
    # 受講者ID（主キー）
    student_id = db.Column("student_id", db.String(10), primary_key=True)
    # 受講者名
    student_name = db.Column("student_name", db.String(50), nullable=False)
    # パスワード
    password = db.Column("password", db.String(12)) 
    # 生年月日
    birthday = db.Column("birthday", db.Date, nullable=False)
    # 通知フラグ
    alert = db.Column("alert", db.Boolean, nullable=False, default=False)
    # グループID（外部キー）
    group_id = db.Column("group_id", db.Integer, db.ForeignKey('group.group_id'))