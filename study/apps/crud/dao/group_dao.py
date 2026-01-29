from sqlalchemy import text
from apps.extensions import db

class GroupDao:
    """ 
    groupテーブル専用のDAOクラス。
    以前発生したタイムアウト（10048エラー）を防ぐため、SQLAlchemy の db.session を使用します。
    """

    def find_all(self):
        """ groupテーブルの全レコードを取得 """
        sql = text("SELECT group_id, group_name, created_by_admin_id FROM `group` ORDER BY group_id ASC")
        return db.session.execute(sql).mappings().all()

    def find_by_admin_id(self, admin_id):
        """ 
        ダッシュボード用：特定の管理者が作成したグループをすべて取得
        """
        sql = text("""
            SELECT group_name AS name, '（説明なし）' AS description, 0 AS member_count
            FROM `group` 
            WHERE created_by_admin_id = :aid
        """)
        # テンプレート側の {{ group.name }} 等に合わせた形式で返します
        return db.session.execute(sql, {"aid": admin_id}).mappings().all()

    def find_by_id(self, group_id):
        """ group_idで1件取得 """
        sql = text("""
            SELECT group_id, group_name, created_by_admin_id 
            FROM `group` 
            WHERE group_id = :gid LIMIT 1
        """)
        return db.session.execute(sql, {"gid": group_id}).mappings().first()

    def insert(self, group_name, admin_id):
        """ 新規登録：提供いただいたバグを修正 """
        sql = text("""
            INSERT INTO `group` (group_name, created_by_admin_id)
            VALUES (:name, :aid)
        """)
        result = db.session.execute(sql, {"name": group_name, "aid": admin_id})
        db.session.commit()
        return result.lastrowid