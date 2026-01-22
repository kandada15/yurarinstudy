from apps.app import db 

# Progress テーブルモデル作成
class Progress(db.Model):
    __tablename__ = 'progress'

    # 学習進捗ID（主キー）
    progress_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # フェーズ名
    phase_name = db.Column(db.String(20), nullable=False)
    # ステージ完了フラグ
    stage_flag = db.Column(db.Boolean, nullable=False, default=False)
    # 受講者ID（外部キー）
    student_id = db.Column(db.String(10), db.ForeignKey('student.student_id'), nullable=False)