# dao_dashboard.py
# Dashboard モデルを MySQL (dashboard テーブル) とやり取りする DAO クラス

import mysql.connector
from mysql.connector import MySQLConnection
from apps.dashboard.models.model_dashboard import Dashboard
from apps.config.db_config import DB_CONFIG  # ★ これを追加


# MySQLに直接アクセスするDAOクラス※progressテーブル専用
class DashboardDao:

    # 初期化処理
    def __init__(self, config: dict | None = None) -> None:
        # DB接続情報を受け取る（指定がなければ DB_CONFIG を使う）
        self.config = config or DB_CONFIG

    # DB接続作成処理
    def _get_connection(self) -> MySQLConnection:
        """MySQL への接続を新しく1つ作って返す"""
        return mysql.connector.connect(**self.config)

    def find_groups_for_progress(self, admin_id: str) -> list[dict]:
        """管理者が作成したグループと、その所属人数を取得します"""
        sql = """
            SELECT 
                g.group_id, 
                g.group_name, 
                COUNT(s.student_id) AS member_count
            FROM `group` g
            LEFT JOIN student s ON g.group_id = s.group_id
            WHERE g.created_by_admin_id = %s
            GROUP BY g.group_id
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (admin_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def find_students_by_group(self, group_id: int) -> list[dict]:
        """特定のグループに所属する生徒のIDと名前、入学年度を取得します"""
        sql = """
        SELECT 
            student_id, 
            student_name, 
            YEAR(created_at) as admission_year 
        FROM student 
        WHERE group_id = %s
    """
        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (group_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_student_stats(self, student_id: str) -> dict:
        """一人の生徒の完了・未完了ステージ数を集計します"""
        sql = """
            SELECT 
                COUNT(*) AS total_count,
                SUM(CASE WHEN stage_flag = 1 THEN 1 ELSE 0 END) AS completed_count
            FROM progress
            WHERE student_id = %s
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (student_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def get_student_detail_list(self, student_id: str) -> list[dict]:
        """一人の生徒の全フェーズの進捗（0 or 1）を取得します"""
        sql = """
            SELECT phase_name, stage_flag 
            FROM progress 
            WHERE student_id = %s 
            ORDER BY progress_id ASC
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (student_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def find_by_admin_id(self, admin_id: str) -> list[dict]:
        """ログイン中の管理者が作成したグループのみを辞書形式で返す"""
        sql = """
            SELECT
            FROM `group`
            WHERE created_by_admin_id = %s
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (admin_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_group_name(self, group_id: int) -> str:
        """IDからグループ名を取得"""
        sql = "SELECT group_name FROM `group` WHERE group_id = %s"
        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (group_id,))
            result = cursor.fetchone()
            return result["group_name"] if result else "不明なグループ"
        finally:
            cursor.close()
            conn.close()

    def find_all_students(self) -> list[dict]:
        """グループに所属していない受講者のIDと名前を取得"""
        sql = """
            SELECT 
            student_id, 
            student_name, 
            YEAR(created_at) as admission_year
            FROM student 
            WHERE group_id IS NULL
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def update_students_group(self, group_id: str, student_ids: list[str]) -> bool:
        """選択された受講生たちの所属グループを更新します"""
        # studentテーブルのgroup_idを書き換えるSQL
        sql = "UPDATE student SET group_id = %s WHERE student_id = %s"

        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            # 1人ずつ順番に更新
            for s_id in student_ids:
                cursor.execute(sql, (group_id, s_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Update Error: {e}")
            conn.rollback()  # 失敗したら元に戻す
            return False
        finally:
            cursor.close()
            conn.close()

    def remove_student_from_group(self, student_id):
        """受講生の所属グループを解除（NULLに更新）します"""
        sql = "UPDATE student SET group_id = NULL WHERE student_id = %s"

        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (student_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Remove Error: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def update_group_name(self, group_id, group_name):
        """特定のグループIDの名前を更新します"""
        sql = "UPDATE `group` SET group_name = %s WHERE group_id = %s"

        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (group_name, group_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Update `Group` Name Error: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def create_group(self, group_name, admin_id):
        """新規グループを登録"""
        get_last_id_sql = "SELECT group_id FROM `group` ORDER BY group_id DESC LIMIT 1"
        insert_sql = "INSERT INTO `group` (group_id, group_name, created_by_admin_id) VALUES (%s, %s, %s)"

        conn = self._get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            # 1. 自動採番
            cursor.execute(get_last_id_sql)
            row = cursor.fetchone()
            new_id = int(row[0]) + 1 if row and row[0] is not None else 1
            # 2. 登録実行
            cursor.execute(insert_sql, (new_id, group_name, admin_id))
            conn.commit()

            return True, f"新規グループ(ID:{new_id})を作成しました"

        except Exception as e:
            print(f"DAO Error: {e}")
            if conn:
                conn.rollback()
            return False, f"登録エラー: {str(e)}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
