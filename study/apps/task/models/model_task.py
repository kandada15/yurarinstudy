from apps.extensions import db

# DBの「task」テーブル
class Task(db.Model):
    __tablename__ = "task"
    # 課題ID(主キー)
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 課題名
    task_name = db.Column(db.String(255))
    # 問題文
    task_text = db.Column(db.Text)