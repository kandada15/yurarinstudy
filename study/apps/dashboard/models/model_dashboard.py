from apps.extensions import db
from dataclasses import dataclass

# Dashboard テーブルモデル作成
class Dashboard(db.Model):
    __tablename__ = "dashboard"

    # ダッシュボードID（主キー）
    dashboard_id = db.Column(db.Integer, primary_key=True)
    dashboard_id = db.Column(db.Integer, primary_key=True)
    # 管理者ID（外部キー）
    admin_id = db.Column(db.String(10), db.ForeignKey('admin.admin_id'))
    # グループID（外部キー）
    group_id = db.Column(db.Integer, db.ForeignKey('group.group_id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.group_id'))
    # 配信済課題ID（外部キー）
    streamed_id = db.Column(db.Integer, db.ForeignKey('streamed.streamed_id'))
    streamed_id = db.Column(db.Integer, db.ForeignKey('streamed.streamed_id'))
    # 提出物ID（外部キー）
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.submission_id'))
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.submission_id'))
    # 学習進捗ID（外部キー）
    progress_id = db.Column(db.Integer, db.ForeignKey('progress.progress_id'))
    progress_id = db.Column(db.Integer, db.ForeignKey('progress.progress_id'))
    # 返却済課題ID（外部キー）
    returned_id = db.Column(db.Integer, db.ForeignKey('returned.returned_id'))

@dataclass
class StreamedStudent:
    student_id: int
    student_name: str
    status: str