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
                    birthday=row["birthday"],
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
        # apps/crud/dao/admin_dao.py の SQL 部分

        sql = """
            SELECT
                admin.admin_id,
                admin.admin_name,
                admin.password,
                admin.birthday,
                admin.admin_id AS created_by_admin_id,
                GROUP_CONCAT(g.group_id) as group_id,
                GROUP_CONCAT(g.group_name) as group_name
            FROM admin
            LEFT JOIN `group` AS g
            ON g.created_by_admin_id = admin.admin_id
            GROUP BY admin.admin_id
            ORDER BY admin.admin_id ASC
        """

        # クラス内部の_get_connection()を使ってMySQL接続を取得
        # 結果を辞書形式で取得
        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            rows = cursor.fetchall()

            # AdminToGroupnameオブジェクトに変換
            result = []
            for row in rows:
                result.append(
                    AdminToGroupname(
                        admin_id=row["admin_id"],
                        admin_name=row["admin_name"],
                        password=row["password"],
                        birthday=row["birthday"],
                        group_id=row["group_id"],
                        group_name=row["group_name"],
                        created_by_admin_id=row["created_by_admin_id"],
                    )
                )
            return result

        finally:
            # 例外の有無に関わらず、最後に必ずクローズする
            cursor.close()
            conn.close()

    #
    def search_admins(self, search_query: str) -> list[AdminToGroupname]:
        """
        admin_id, admin_name, group_name のいずれかに
        検索ワードが含まれるレコードを取得
        """
        sql = """
            SELECT
                admin.admin_id,
                admin.admin_name,
                admin.password,
                admin.birthday,
                admin.admin_id AS created_by_admin_id,
                GROUP_CONCAT(g.group_id) as group_id,
                GROUP_CONCAT(g.group_name) as group_name
            FROM admin
            LEFT JOIN `group` AS g
            ON g.created_by_admin_id = admin.admin_id
            WHERE 
                admin.admin_id LIKE %s OR
                admin.admin_name LIKE %s OR
                g.group_name LIKE %s
            GROUP BY admin.admin_id
            ORDER BY admin.admin_id ASC
        """

        # 部分一致検索
        like_query = f"%{search_query}%"
        params = (like_query, like_query, like_query)

        # クラス内部の_get_connection()を使ってMySQL接続を取得
        # 結果を辞書形式で取得
        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, params)
            rows = cursor.fetchall()

            # AdminToGroupname
            result = []
            for row in rows:
                result.append(
                    AdminToGroupname(
                        admin_id=row["admin_id"],
                        admin_name=row["admin_name"],
                        password=row["password"],
                        birthday=row["birthday"],
                        group_id=row["group_id"],
                        group_name=row["group_name"],
                        created_by_admin_id=row["created_by_admin_id"],
                    )
                )

            return result

        finally:
            # 例外の有無に関わらず、最後に必ずクローズする
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
            # 例外の有無に関わらず、最後に必ずクローズする
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
    
    def reset_password(self, admin_id: str) -> bool:
        # DATE_FORMAT で誕生日を 'YYYYMMDD' 形式の文字列に変換してパスワードに設定
        sql = """
            UPDATE admin 
            SET password = DATE_FORMAT(birthday, '%Y%m%d') 
            WHERE admin_id = %s
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (admin_id,))
            conn.commit()
            return cursor.rowcount > 0 # 更新された行があればTrue
        finally:
            cursor.close()
            conn.close()
    
    def delete_admin(self, admin_id: str) -> bool:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()

            sql_get_groups = "SELECT group_id FROM `group` WHERE created_by_admin_id = %s"
            cursor.execute(sql_get_groups, (admin_id,))
            groups = cursor.fetchall()
            
            if groups:
                # group_id のリストを作成 (例: [1, 2, 3])
                group_ids = [g['group_id'] if isinstance(g, dict) else g[0] for g in groups]
                format_strings = ','.join(['%s'] * len(group_ids))
                sql_delete_mypage = f"DELETE FROM mypage WHERE group_id IN ({format_strings})"
                cursor.execute(sql_delete_mypage, tuple(group_ids))
            
            
            sql_group = "DELETE FROM `group` WHERE created_by_admin_id = %s"
            cursor.execute(sql_group, (admin_id,))
            sql_admin = "DELETE FROM admin WHERE admin_id = %s"
            cursor.execute(sql_admin, (admin_id,))
            
            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            # どこかで失敗したらすべて元に戻す
            conn.rollback()
            print(f"管理者削除エラー: {e}")
            raise e
        finally:
            cursor.close()
            conn.close()

    def _get_table_info(self, user_type):
        """
        種別に応じて (テーブル名, IDカラム名) を返す
        """
        if user_type == "admin":
            return "admin", "admin_id", "admin_name"
        else:
            return "student", "student_id", "student_name"

    def check_id_exists(self, u_id, user_type):
        """IDの重複チェック"""
        table_name, id_column, _ = self._get_table_info(user_type)
        sql = f"SELECT COUNT(*) FROM {table_name} WHERE {id_column} = %s"
        
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (u_id,))
            result = cursor.fetchone()
            return result[0] > 0
        finally:
            cursor.close()
            conn.close()

    def register_user(self, u_id, name, password, birthday, user_type):
        table_name, id_column, name_column = self._get_table_info(user_type)
        
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            # 1. 基本情報の登録 (admin または student)
            if user_type == "admin":
                sql_main = f"INSERT INTO {table_name} ({id_column}, {name_column}, password, birthday, created_at) VALUES (%s, %s, %s, %s, NOW())"
                params_main = (u_id, name, password, birthday)
            else:
                sql_main = f"INSERT INTO {table_name} ({id_column}, {name_column}, password, birthday, alert, created_at) VALUES (%s, %s, %s, %s, %s, NOW())"
                params_main = (u_id, name, password, birthday, 0)
            
            cursor.execute(sql_main, params_main)

            # 受講生の場合、progressテーブルに20行追加
            if user_type == "student":
                phases = ["①", "②", "③", "④"]
                steps = ["1理解", "2構成", "3思考", "4表現", "5実践"]
                
                # 20個のフェーズ名を生成
                phase_names = [f"{p}-{s}" for p in phases for s in steps]
                
                sql_progress = """
                    INSERT INTO progress (phase_name, stage_flag, student_id) 
                    VALUES (%s, 0, %s)
                """
                
                # ループで20回実行
                for p_name in phase_names:
                    cursor.execute(sql_progress, (p_name, u_id))

            conn.commit()
            return True

        except Exception as e:
            print(f"【DAO ERROR】一括登録に失敗しました: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()