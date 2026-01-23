from apps.extensions import db

# ADMIN テーブルモデル作成
class Admin(db.Model):
    __tablename__ = 'admin'
    
    # 管理者ID（主キー）
    admin_id = db.Column(db.String(10), primary_key=True)
    # 管理者名
    admin_name = db.Column(db.String(50), nullable=False)
    # パスワード
    password = db.Column(db.String(255), nullable=False)

# GROUP テーブルモデル作成
class GROUP(db.Model):
    __tablename__ = 'GROUP'
    
    # グループID（主キー）
    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # グループ名
    group_name = db.Column(db.String(50), nullable=False)
    # 管理者ID（外部キー）
    admin_id = db.Column(db.String(10), db.ForeignKey('admin.admin_id'))