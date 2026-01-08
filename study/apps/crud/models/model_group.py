from apps.extensions import db

class Group(db.Model):
    __tablename__ = "group"

    # db.Column を使って定義します
    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_name = db.Column(db.String(50))
    
    # 外部キー（Adminとの紐付け）
    created_by_admin_id = db.Column(db.String(255), db.ForeignKey('admin.admin_id'))

    # リレーション（紐付いているStudentにアクセスしやすくする設定）
    # これがあると group.students でそのグループの生徒一覧が取れるようになります
    students = db.relationship('Student', backref='group_orders', lazy='dynamic')