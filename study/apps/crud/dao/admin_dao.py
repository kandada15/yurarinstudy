import mysql.connector
from mysql.connector import MySQLConnection
from typing import Optional
from apps.crud.models.model_admin import Admin, AdminToGroupname
from apps.config.db_config import DB_CONFIG

# MySQLに直接アクセスするDAOクラス※adminテーブル専用
class AdminDao:

    # 初期化処理
    def __init__(self, config: dict | None = None) -> None:
        self.config = config or DB_CONFIG

    # DB接続作成処理
    def _get_connection(self) -> MySQLConnection:
        return mysql.connector.connect(**self.config)

    # 全件取得
    def find_all(self) -> list[Admin]:
        """ 
        adminテーブルの全レコードを取得
        Adminオブジェクトのリストとして返す。
        管理者情報をadmin_id順で取得
        """
        sql = """
            SELECT
                admin_id,
                admin_name,
                password,
                birthday
            FROM admin
            ORDER BY admin_id ASC
        """

        # クラス内部の_get_connection()を使ってMySQL接続を取得
        # 結果を辞書形式で取得
        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            rows = cursor.fetchall()

            # Adminオブジェクトに変換
            admins: list[Admin] = []
            for row in rows:
                admin = Admin(
                    admin_id=row["admin_id"],
                    admin_name=row["admin_name"],
                    password=row["password"],
                    birthday=row["birthday"]
                )
                admins.append(admin)

            return admins
        finally:
            cursor.close()
            conn.close()

    # 全件取得
    def find_all_groupname(self) -> list[AdminToGroupname]:
        """ 
        adminテーブルの全レコードを取得
        Adminオブジェクトのリストとして返す。
        管理者情報をadmin_id順で取得
        """
        sql = """
            SELECT
                admin.admin_id,
                admin.admin_name,
                admin.password,
                admin.birthday,
                g.group_id,
                g.group_name,
                g.created_by_admin_id
            FROM admin
            LEFT OUTER JOIN `group` AS g
              ON g.created_by_admin_id = admin.admin_id
            ORDER BY admin_id ASC
        """

        # クラス内部の_get_connection()を使ってMySQL接続を取得
        # 結果を辞書形式で取得
        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            rows = cursor.fetchall()

            # Adminオブジェクトに変換
            result = []
            for row in rows:
                result.append(AdminToGroupname(
                    admin_id=row["admin_id"],
                    admin_name=row["admin_name"],
                    password=row["password"],
                    birthday=row["birthday"],
                    group_id=row["group_id"],
                    group_name=row["group_name"],
                    created_by_admin_id=row["created_by_admin_id"]
                ))
            return result
        finally:
            cursor.close()
            conn.close()

    def search_admins(self, search_query: str) -> list[AdminToGroupname]:
        """  
        admin_id, admin_name, group_name のいずれかに
        検索キーワードが含まれるレコードを取得する。
        """

        sql = """
            SELECT
                admin.admin_id,
                admin.admin_name,
                admin.password,
                admin.birthday,
                g.group_id,
                g.group_name,
                g.created_by_admin_id
            FROM admin
            LEFT JOIN `group` AS g
              ON g.created_by_admin_id = admin.admin_id
            WHERE 
                admin.admin_id LIKE %s OR
                admin.admin_name LIKE %s OR
                g.group_name LIKE %s
            ORDER BY admin.admin_id ASC
        """

        like_query = f"%{search_query}%"
        params = (like_query, like_query, like_query)

        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, params)
            rows = cursor.fetchall()

            result = []
            for row in rows:
                result.append(AdminToGroupname(
                    admin_id=row["admin_id"],
                    admin_name=row["admin_name"],
                    password=row["password"],
                    birthday=row["birthday"],
                    group_id=row["group_id"],
                    group_name=row["group_name"],
                    created_by_admin_id=row["created_by_admin_id"]
                ))

            return result

        finally:
            cursor.close()
            conn.close()


    # admin ID検索
    def find_by_id(self, admin_id: str) -> Optional[dict]:
        """ 
        admin_idで admin テーブルから1件取得。見つからなければNoneを返す。
        戻り値: 辞書型 {"admin_id":..., "admin_name":...}
        %s はプレースホルダー
        """
        sql = """
            SELECT
                admin_id,
                admin_name,
                password,
                birthday,
                entry_date
            FROM admin
            WHERE admin_id = %s
            LIMIT 1
        """

        # クラス内部の_get_connection()を使ってMySQL接続を取得
        # 結果を辞書形式で取得
        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (admin_id,))
            row = cursor.fetchone()
            return row
        finally:
            cursor.close()
            conn.close()

    # admin新規登録
    def insert(self, admin_id: str, admin_name: str, password: str, birthday) -> str:
        """
        insert文にて管理者を追加
        AdminはIDが自動採番ではないため、引数で受け取ったadmin_idをそのまま返す
        """
        sql = """
            INSERT INTO admin
                (admin_id, admin_name, password, birthday, entry_date)
            VALUES
                (%s, %s, %s, %s, NOW())
        """

        # クラス内部の_get_connection()を使ってMySQL接続を取得
        # 実行＆コミット
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (admin_id, admin_name, password, birthday))
            conn.commit()
            return admin_id
        
        finally:
            # 例外の有無に関わらず、最後に必ずクローズする
            cursor.close()
            conn.close()