from apps.extensions import db
from datetime import datetime

class Admin(db.Model):
    __tablename__ = "admin"

    # DBのカラム名に合わせて定義
    admin_id = db.Column("admin_id", db.String(10), primary_key=True)
    admin_name = db.Column("admin_name", db.String(50), nullable=False)
    
    # ★修正点: DBのカラム名は 'password' なので、それに合わせます
    # 'password_hash' にすると Unknown column エラーになります
    password = db.Column("password", db.String(255), nullable=False)
    
    birthday = db.Column("birthday", db.Date, nullable=False)
