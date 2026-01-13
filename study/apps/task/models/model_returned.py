from apps.extensions import db

# DBの「return」テーブル
class Returned(db.Model):
      __tablename__ = "returned"
      # 課題返却ID(主キー)
      returned_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
      # 添削文
      check_text = db.Column(db.Text)
      # 回答文
      q_a_t = db.Column(db.Text)
      # 提出物ID(外部キー)
      submission_id = db.Column(db.Integer, db.ForeignKey('submission.submission_id'))
      
      a