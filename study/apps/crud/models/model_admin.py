from apps.extensions import db
from datetime import datetime

# Admin テーブルモデル作成
class Admin(db.Model):
    __tablename__ = "admin"

    # 管理者ID（主キー）
    admin_id = db.Column("admin_id", db.String(10), primary_key=True)
    # 管理者名
    admin_name = db.Column("admin_name", db.String(50), nullable=False)
    # パスワード
    password = db.Column("password", db.String(255), nullable=False)
    #生年月日
    birthday = db.Column("birthday", db.Date, nullable=False)