from apps.app import db
from datetime import datetime
from sqlalchemy import ForeignKey
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(db.Model, UserMixin):
    __tablename__ = 'admins'
    admin_id = db.Column(db.String(10), primary_key=True)
    admin_name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(12), nullable=False,)
    admin_class = db.Column(db.String(20), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    entry_date = db.Column(db.DateTime, default=datetime.now)
    group_id = db.Column(db.String(10), db.ForeignKey('group.group_id'))

    # passwordという直接アクセスできない属性を定義
    @property
    def password(self):
        raise AttributeError("読み取り不可") # passwordにアクセスするとエラーになる
    
    ## passwordに値を代入する処理
    # passwordに値を入れようとすると以下の関数が実行される
    @password.setter 

    # パスワードをハッシュ化するメソッドを定義
    def password(self, password): 
        # パスワードをハッシュ化してpassword_hashに保存
        self.password_hash = generate_password_hash(password) 

    # パスワードの検証
    def verify_password(self, password): 
        return check_password_hash(self.password_hash, password)


class Student(db.Model, UserMixin):
    __tablename__ = 'students'
    student_id = db.Column(db.String(10), primary_key=True, nullable=False)
    student_name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(12), nullable=False)
    entry_year = db.Column(db.Integer, nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    entry_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    is_alert = db.Column(db.Boolean, default=False)
    group_id = db.Column(db.String(10), db.ForeignKey('group.group_id'))

    # passwordという直接アクセスできない属性を定義
    @property
    def password(self):
        raise AttributeError("読み取り不可") # passwordにアクセスするとエラーになる
    
    ## passwordに値を代入する処理
    # passwordに値を入れようとすると以下の関数が実行される
    @password.setter 

    # パスワードをハッシュ化するメソッドを定義
    def password(self, password): 
        # パスワードをハッシュ化してpassword_hashに保存
        self.password_hash = generate_password_hash(password) 

    # パスワードの検証
    def verify_password(self, password): 
        return check_password_hash(self.password_hash, password)

class Group(db.Model):
    __tablename__ = 'group'
    group_id = db.Column(db.String(10), primary_key=True, nullable=False)
    group_name = db.Column(db.String(20), nullable=False)
    admin_name = db.Column(db.String(255), nullable=False)



  
