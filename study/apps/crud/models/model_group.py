from apps.extensions import db

# Group テーブルモデル作成
class Group(db.Model):
    __tablename__ = "group"

    # DBのカラム名に合わせて定義
    group_id = db.Column("group_id", db.Integer, primary_key=True, autoincrement=True)
    group_name = db.Column("group_name", db.String(50), nullable=False)
    admin_id = db.Column("created_by_admin_id", db.String(10), db.ForeignKey('admin.admin_id'))