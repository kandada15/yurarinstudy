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
        """特定のグループに所属する生徒のIDと名前を取得します"""
        sql = "SELECT student_id, student_name FROM student WHERE group_id = %s"
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
        """ ログイン中の管理者が作成したグループのみを辞書形式で返す """
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