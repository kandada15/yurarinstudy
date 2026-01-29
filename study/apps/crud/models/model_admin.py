from apps.extensions import db
from datetime import date

from dataclasses import dataclass

# Admin テーブルモデル作成
class Admin(db.Model):
    __tablename__ = "admin"

    # 管理者ID（主キー）
    admin_id = db.Column(db.String(10), primary_key=True)
    # 管理者名
    admin_name = db.Column(db.String(50), nullable=False)
    # パスワード
    password = db.Column(db.String(12), nullable=False)
    # 生年月日
    birthday = db.Column(db.Date, nullable=False)
    # 登録日時
    created_at = db.Column(db.DateTime, nullable=True)

@dataclass
class AdminToGroupname:
    __tablename__ = "admintogroupname"
    admin_id: int
    admin_name:str
    password: str
    birthday: date
    group_id: int
    group_name: str
    created_by_admin_id: int
