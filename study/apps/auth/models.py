from apps.extensions import db

# 管理者テーブル
class Admin(db.Model):
    __tablename__ = 'ADMIN'
    admin_id = db.Column("ADMIN_ID", db.String(10), primary_key=True)
    admin_name = db.Column("ADMIN_NAME", db.String(50), nullable=False)
    password = db.Column("PASSWORD", db.String(255), nullable=False)

# グループテーブル
class Group(db.Model):
    __tablename__ = 'GROUP'
    group_id = db.Column("GROUP_ID", db.Integer, primary_key=True, autoincrement=True)
    group_name = db.Column("GROUP_NAME", db.String(50), nullable=False)
    # 管理者との紐付け（外部キー）
    admin_id = db.Column("ADMIN_ID", db.String(10), db.ForeignKey('ADMIN.ADMIN_ID'))