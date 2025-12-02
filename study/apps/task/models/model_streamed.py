from apps.extensions import db

class Streamed(db.Model):
    __tablename__ = "streamed"
    # 配信済み課題ID(主キー)
    streamed_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 課題提出期限
    streamed_limit = db.Column(db.DateTime)
    # 課題ID(外部キー)
    task_id = db.Column(db.Integer, db.ForeignKey('task.task_id'))
    # グループID(外部キー)
    group_id = db.Column(db.Integer, db.ForeignKey('group.group_id'))