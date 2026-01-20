from apps.extensions import db
from datetime import datetime

# Student テーブルモデル作成
class Student(db.Model):
    __tablename__ = 'student'
    
    # DBのカラム名に合わせて定義
    # --- 必須のカラム（データベースにあるものだけ） ---
    student_id = db.Column("student_id", db.String(10), primary_key=True)
    student_name = db.Column("student_name", db.String(50), nullable=False)
    password = db.Column("password", db.String(12)) 
    
    # 誕生日
    birthday = db.Column("birthday", db.Date, nullable=False)
    
    alert = db.Column("alert", db.Boolean, nullable=False, default=False)
    
    # グループID
    group_id = db.Column("group_id", db.Integer, db.ForeignKey('group.group_id'))