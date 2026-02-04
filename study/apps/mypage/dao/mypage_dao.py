from sqlalchemy import text
from apps.extensions import db
import mysql.connector
from mysql.connector import MySQLConnection
from apps.config.db_config import DB_CONFIG

class MypageDao:
    
    # 1. 初期化処理：DashboardDaoと共通の設定を読み込む
    def __init__(self, config: dict | None = None) -> None:
        self.config = config or DB_CONFIG

    # 2. mysql-connector用の接続作成メソッド
    def _get_connection(self) -> MySQLConnection:
        """MySQL への接続を新しく1つ作って返す"""
        return mysql.connector.connect(**self.config)

    # ==========================================
    # 受講生マイページトップ用 (SQLAlchemy使用)
    # ==========================================

    def get_user_profile(self, user_id):
        """受講生の基本プロフィールを取得"""
        sql = text("""
            SELECT student_id, student_name, birthday
            FROM student 
            WHERE student_id = :uid
        """)
        return db.session.execute(sql, {"uid": user_id}).mappings().first()

    def get_task_summary(self, user_id):
        """課題の提出状況（未提出・提出済・返却済）を集計"""
        sql = text("""
            SELECT 
                SUM(CASE WHEN submit_flag = 0 THEN 1 ELSE 0 END) as pending,
                SUM(CASE WHEN submit_flag = 1 THEN 1 ELSE 0 END) as submitted,
                SUM(CASE WHEN return_flag = 1 THEN 1 ELSE 0 END) as returned
            FROM submission
            WHERE student_id = :uid
        """)
        result = db.session.execute(sql, {"uid": user_id}).mappings().first()
        return {
            'pending': result['pending'] or 0,
            'submitted': result['submitted'] or 0,
            'returned': result['returned'] or 0
        }

    def get_writing_progress(self, user_id):
        """ライティング学習の全体進捗（円グラフ用）"""
        sql = text("""
            SELECT 
                SUM(CASE WHEN stage_flag = 1 THEN 1 ELSE 0 END) as completed,
                COUNT(*) as total
            FROM progress 
            WHERE student_id = :uid
        """)
        return db.session.execute(sql, {"uid": user_id}).mappings().first()
  
    def get_user_group(self, user_id):
        """所属グループの情報とメンバー数を取得"""
        sql = text("""
            SELECT 
                g.group_name,
                (SELECT COUNT(*) FROM student s2 WHERE s2.group_id = g.group_id) AS member_count
            FROM student s1
            JOIN `group` g ON s1.group_id = g.group_id
            WHERE s1.student_id = :uid
        """)
        return db.session.execute(sql, {"uid": user_id}).mappings().first()
    
    # ==========================================
    # 管理者向け詳細画面用 (DashboardDaoと共通スタイル)
    # ==========================================

    def get_student_stats(self, student_id: str) -> dict:
        """一人の生徒の完了・未完了ステージ数を集計"""
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
            result = cursor.fetchone()
            if result:
                result['total_count'] = result['total_count'] or 0
                # SUMの結果がNoneになる場合があるため int() で安全に変換
                result['completed_count'] = int(result['completed_count']) if result['completed_count'] else 0
            return result
        finally:
            cursor.close()
            conn.close()

    def get_student_detail_list(self, student_id: str) -> list[dict]:
        """フェーズごとの進捗詳細を一覧取得"""
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