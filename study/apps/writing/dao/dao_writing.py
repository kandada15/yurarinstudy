from sqlalchemy import text
from apps.extensions import db


# MySQLに直接アクセスするDAOクラス※progressテーブル専用
class WritingDao:

    # 初期化処理
    def __init__(self):
        self.symbol_map = {1: "①", 2: "②", 3: "③", 4: "④"}

    # カテゴリIDに応じたカテゴリ名を返す
    def get_category_name(self, category_id):
        categories = {
            1: "小論文",
            2: "ビジネス文書",
            3: "レポート",
            4: "表現トレーニング",
        }
        return categories.get(category_id, "ライティング学習")

    # 進捗を取得
    def get_user_progress(self, student_id, category_id):

        # カテゴリIDに応じて①～④を取得
        symbol = self.symbol_map.get(category_id, "①")

        # progressテーブルからフェーズ名,学習状況を取得
        sql = text(
            """
            SELECT phase_name, stage_flag 
            FROM progress 
            WHERE student_id = :sid AND phase_name LIKE :prefix
        """
        )

        # カテゴリに対応するステップを表示
        return (
            db.session.execute(sql, {"sid": student_id, "prefix": f"{symbol}-%"})
            .mappings()
            .all()
        )

    # 学習状況更新
    def update_stage_progress(self, student_id, phase_name):
        """指定されたステップのstage_flagを1(完了)に更新"""
        sql = text(
            """
            UPDATE progress 
            SET stage_flag = 1 
            WHERE student_id = :sid AND phase_name = :pname
            """
        )

        # SQL実行
        result = db.session.execute(sql, {"sid": student_id, "pname": phase_name})

        # デバッグログ
        print(f"--- デバッグ: 更新対象フェーズ: {phase_name} ---")
        print(f"--- デバッグ: 更新成功件数: {result.rowcount} ---")

        # コミット
        db.session.commit()