from apps.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Student(db.Model):
    __tablename__ = "student"

    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_name = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    
    # 日付系
    entry_year = db.Column(db.Date)
    birthday = db.Column(db.Date)
    entry_date = db.Column(db.Date, default=datetime.now)
    
    is_alert = db.Column(db.Boolean, default=False)
    
    # 外部キー（Groupとの紐付け）
    group_id = db.Column(db.Integer, db.ForeignKey('group.group_id'))

    # パスワード設定用プロパティ
    @property
    def password(self):
        raise AttributeError("読み取り不可")
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)