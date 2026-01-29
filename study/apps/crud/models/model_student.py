from apps.extensions import db
from dataclasses import dataclass
from datetime import date, datetime

# Student テーブルモデル作成
class Student(db.Model):
    __tablename__ = 'student'
    
    # 受講者ID（主キー）
    student_id = db.Column(db.String(10), primary_key=True)
    # 受講者名
    student_name = db.Column(db.String(50), nullable=False)
    # パスワード
    password = db.Column(db.String(12)) 
    # 生年月日
    birthday = db.Column(db.Date, nullable=False)
    # 登録日時
    created_at = db.Column(db.DateTime, nullable=True)
    # 通知フラグ
    alert = db.Column(db.Boolean, nullable=False, default=False)
    # グループID（外部キー）
    group_id = db.Column(db.Integer, db.ForeignKey('group.group_id'))

@dataclass
class StudentToGroupname:
    __tablename__ = "studenttogroupname"
    student_id: int
    student_name: str
    password: str 
    # 生年月日
    birthday: date
    # 通知フラグ
    alert: bool
    # グループID（外部キー）
    group_id: int
    group_name: str