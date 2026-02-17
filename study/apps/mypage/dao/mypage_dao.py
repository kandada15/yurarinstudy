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

    # 受講生の基本プロフィール（ID、氏名、誕生日）を取得
    def get_user_profile(self, user_id):
        """受講生の基本プロフィールを取得"""
        sql = text("""
            SELECT student_id, student_name, birthday
            FROM student 
            WHERE student_id = :uid
        """)
        return db.session.execute(sql, {"uid": user_id}).mappings().first()

    # 課題の「未完了・提出済み・返却済み」の件数をそれぞれ集計
    def get_task_summary(self, user_id):
        """課題の提出状況（未提出・提出済・返却済）を集計"""
        sql = text("""
            SELECT 
                -- 提出フラグが0、または提出データ自体がない（NULL）場合は「未完了」
                SUM(CASE WHEN sub.submit_flag = 0 OR sub.submit_flag IS NULL THEN 1 ELSE 0 END) as pending,
                
                -- 提出フラグが1なら「提出済」
                SUM(CASE WHEN sub.submit_flag = 1 THEN 1 ELSE 0 END) as submitted,
                
                -- 返却フラグが1なら「返却済(returned)」
                SUM(CASE WHEN sub.return_flag = 1 THEN 1 ELSE 0 END) as returned
                
            FROM streamed st
            -- 受講生が所属しているグループの課題を紐付け
            JOIN student s ON st.group_id = s.group_id
            -- 提出データを結合（まだない場合はNULL）
            LEFT JOIN submission sub ON st.streamed_id = sub.streamed_id 
                                    AND sub.student_id = s.student_id
            WHERE s.student_id = :uid
        """)
        result = db.session.execute(sql, {"uid": user_id}).mappings().first()
        return {
            'pending': result['pending'] or 0,
            'submitted': result['submitted'] or 0,
            'returned': result['returned'] or 0
        }

    # ライティング学習の進捗状況を、完了数と総数で取得
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

    # 自分が所属しているグループの名前と、同じグループに何人のメンバーがいるかを取得
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

    # 【管理者用】特定の生徒が全20ステージのうち何ステージ完了しているかを数値で集計
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

    # 【管理者用】全フェーズのリストを取得し、どこが完了（1）でどこが未完了（0）かを一覧で取得
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

    # 受講生自身のパスワードを新しいものに更新
    def update_password(self, user_id, new_password):
        sql = "UPDATE student SET password = %s WHERE student_id = %s" 
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (new_password, user_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            conn.close()

    # 先生から「返却」された課題の一覧を、提出日時の新しい順に取得
    def get_returned_tasks(self, user_id):
        """返却済みの課題一覧を取得（配信日時の新しい順）"""
        sql = text("""
            SELECT 
                s.submitted_at, 
                st.streamed_name, 
                a.admin_name, 
                st.streamed_limit,
                s.streamed_id
            FROM submission s
            JOIN streamed st ON s.streamed_id = st.streamed_id
            JOIN `group` g ON st.group_id = g.group_id
            JOIN admin a ON g.created_by_admin_id = a.admin_id
            WHERE s.student_id = :uid 
            AND s.return_flag = 1
            ORDER BY s.submitted_at DESC
        """)
        
        result = db.session.execute(sql, {"uid": user_id}).mappings().all()
        return result
    
    # 特定の返却済み課題について、問題文・自分の解答・先生の添削文をセットで取得
    def get_returned_task_detail(self, user_id, streamed_id):
        """特定の返却済み課題の詳細を取得（添削文を含む）"""
        sql = text("""
            SELECT 
                st.streamed_name,
                st.streamed_text,     -- 問題文
                s.answer_text,        -- 自分の解答
                r.check_text,         -- 添削文（returnedテーブル）
                a.admin_name
            FROM submission s
            JOIN streamed st ON s.streamed_id = st.streamed_id
            JOIN returned r ON s.submission_id = r.submission_id
            JOIN `group` g ON st.group_id = g.group_id
            JOIN admin a ON g.created_by_admin_id = a.admin_id
            WHERE s.student_id = :uid 
                AND s.streamed_id = :sid
        """)
        
        result = db.session.execute(sql, {"uid": user_id, "sid": streamed_id}).mappings().first()
        return result