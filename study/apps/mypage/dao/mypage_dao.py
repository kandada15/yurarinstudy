from sqlalchemy import text
from apps.extensions import db

class MypageDao:
    def get_user_profile(self, user_id):
        """ユーザー情報の取得"""
        sql = text("SELECT * FROM student WHERE user_id = :uid")
        return db.session.execute(sql, {"uid": user_id}).mappings().first()

    def get_task_summary(self, user_id):
        """image_654d1f.png のフラグに基づいた課題集計"""
        sql = text("""
            SELECT 
                SUM(CASE WHEN submit_flag = 0 THEN 1 ELSE 0 END) as pending,
                SUM(CASE WHEN submit_flag = 1 THEN 1 ELSE 0 END) as submitted,
                SUM(CASE WHEN return_flag = 1 THEN 1 ELSE 0 END) as returned
            FROM submission
            WHERE student_id = :uid
        """)
        result = db.session.execute(sql, {"uid": user_id}).mappings().first()
        # データがない場合に 0 を返すように処理
        return {
            'pending': result['pending'] or 0,
            'submitted': result['submitted'] or 0,
            'returned': result['returned'] or 0
        }

    def get_writing_progress(self, user_id):
        """ライティング学習の進捗（完了数/全ステージ数）"""
        sql = text("""
            SELECT 
                SUM(CASE WHEN stage_flag = 1 THEN 1 ELSE 0 END) as completed,
                COUNT(*) as total
            FROM progress 
            WHERE student_id = :uid
        """)
        return db.session.execute(sql, {"uid": user_id}).mappings().first()