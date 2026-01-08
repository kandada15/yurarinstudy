from apps.extensions import db
from datetime import datetime

# DBの「submission」テーブル
class Submission(db.Model):
    __tablename__ = "submission"
    # 提出物ID(主キー)
    submission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 解答文
    answer_text = db.Column(db.Text)
    # 質問文
    q_t = db.Column(db.Text)
    # 課題提出フラグ
    submit_flag = db.Column(db.Boolean, default=False)
    # 提出日時
    submit_date = db.Column(db.DateTime, default=datetime.now)
    # 提出課題添削フラグ
    check_flag = db.Column(db.Boolean, default=False)
    # 提出課題返却フラグ
    return_flag = db.Column(db.Boolean, default=False)
    # 課題ID(外部キー)
    task_id = db.Column(db.Integer, db.ForeignKey('task.task_id'))
    # 受講者ID(外部キー)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'))