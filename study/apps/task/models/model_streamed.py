from apps.extensions import db

# Streamed テーブルモデル作成
class Streamed(db.Model):
    __tablename__ = "streamed"
    # 配信済課題ID（主キー）
    streamed_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 課題名
    streamed_name = db.Column(db.String(255))
    # 問題文
    streamed_text = db.Column(db.String(255))
    # 課題提出期限
    streamed_limit = db.Column(db.DateTime)
    # グループID（外部キー）
    group_id = db.Column(db.Integer, db.ForeignKey('group.group_id'))