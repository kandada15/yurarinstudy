from apps.app import db 

class Progress(db.Model):
    # MySQLのテーブル名を指定
    __tablename__ = 'progress'

    progress_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phase_name = db.Column(db.String(20), nullable=False)
    stage_flag = db.Column(db.Boolean, nullable=False, default=False)
    student_id = db.Column(db.String(10), db.ForeignKey('student.student_id'), nullable=False)

    def __repr__(self):
        return f"<Progress(id={self.progress_id}, phase={self.phase_name}, flag={self.stage_flag})>"