from apps.extensions import db
from datetime import datetime
from dataclasses import dataclass

class Streamed(db.Model):
    __tablename__ = "streamed"
    # 配信済み課題ID(主キー)
    streamed_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 課題提出期限
    streamed_name = db.Column(db.String(255))
    streamed_text = db.Column(db.String(255))
    streamed_limit = db.Column(db.DateTime)
    # グループID(外部キー)
    group_id = db.Column(db.Integer, db.ForeignKey('group.group_id'))
@dataclass
class StreamedForStudent:
    __tablename__ = "streamedforstudent"
    streamed_id : int
    streamed_name: str
    streamed_limit: datetime  
    sent_at: datetime
    admin_name: str | None