from sqlalchemy import text
from apps.extensions import db

class WritingDao:
    def __init__(self):
        self.symbol_map = {1: '①', 2: '②', 3: '③', 4: '④'}

    def get_category_name(self, category_id):
        categories = {1: "小論文", 2: "ビジネス文書", 3: "レポート", 4: "表現トレーニング"}
        return categories.get(category_id, "ライティング学習")

    def get_user_progress(self, student_id, category_id):
        """LIKE検索でカテゴリ別の進捗を取得"""
        symbol = self.symbol_map.get(category_id, '①')
        sql = text("""
            SELECT phase_name, stage_flag 
            FROM progress 
            WHERE student_id = :sid AND phase_name LIKE :prefix
        """)
        return db.session.execute(sql, {
            "sid": student_id, 
            "prefix": f"{symbol}-%"
        }).mappings().all()

    def update_stage_progress(self, student_id, phase_name):
        # まずは UPDATE を試みる
        update_sql = text("""
            UPDATE progress SET stage_flag = 1 
            WHERE student_id = :sid AND phase_name = :pname
        """)
        result = db.session.execute(update_sql, {"sid": student_id, "pname": phase_name})
        
        # もし1件も更新されなかったら（＝レコードが存在しない）、新規作成する
        if result.rowcount == 0:
            insert_sql = text("""
                INSERT INTO progress (student_id, phase_name, stage_flag)
                VALUES (:sid, :pname, 1)
            """)
            db.session.execute(insert_sql, {"sid": student_id, "pname": phase_name})
        
        db.session.commit()