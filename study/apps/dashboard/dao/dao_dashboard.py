# dao_dashboard.py
# Dashboard モデルを MySQL (dashboard テーブル) とやり取りする DAO クラス

import mysql.connector
from mysql.connector import MySQLConnection
from models.model_dashboard import Dashboard
from config.db_config import DB_CONFIG  # ★ これを追加

# # ※ 本番環境では環境変数や設定ファイルに出すべきですが、
# #    学習用なのでここに直接書いています。
# DB_CONFIG = {
#     "host": "localhost",  # MySQL サーバ（自分のPCなら localhost）
#     "user": "root",  # MySQL のユーザー名（環境に合わせて変更）
#     "password": "20260210",  # ↑ あなたのパスワードに変更してください
#     "database": "study",  # 先ほど作成した DB 名
# }


class Dashboard_DAO:
    """progress テーブルにアクセスするための DAO クラス"""

    # 初期化メソッド
    def __init__(self, config: dict | None = None) -> None:
        # DB接続情報を受け取る（指定がなければ DB_CONFIG を使う）
        self.config = config or DB_CONFIG

    def _get_connection(self) -> MySQLConnection:
        """MySQL への接続を新しく1つ作って返す"""
        return mysql.connector.connect(**self.config)

    def find_all(self) -> list[Dashboard]:
        """
        progress テーブルの全レコードを取得して、
        Progress オブジェクトのリストとして返す
        ※複数件をまとめて返す
        """
        sql = """
            SELECT
                d.DASHBOARD_ID,
                
                -- 管理者情報
                a.ADMIN_ID,
                a.ADMIN_NAME,
                a.GRROUP_NAME
                
                -- グループ情報
                g.GROUP_NAME,
                g.ADMIN_NAME AS GROUP_ADMIN_NAME,
                
                -- 配信済課題情報
                -- 累計課題配信数
                
                -- 未添削課題数
                
                -- 提出済課題数
                
                -- 未提出課題数
                
                -- 学習進捗(遷移するだけ)
                
                
    
                -- 返却済課題(遷移するだけ)

            FROM DASHBOARD d
            JOIN ADMIN a ON d.ADMIN_ID = a.ADMIN_ID
            JOIN GROUP g ON d.GROUP_ID = g.GROUP_ID
            JOIN PROGRESS p ON d.PROGRESS_ID = p.PROGRESS_ID
            JOIN TASK t ON d.TASK_ID = t.TASK_ID
            OIN SUBMISSION s ON d.SUBMISSION_ID = s.SUBMISSION_ID;
        """

        conn = self._get_connection()
        try:
            # dictionary=True にすると、結果が dict 形式で返る（列名でアクセスできる）
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            rows = cursor.fetchall()

            dashboards: list[Dashboard] = []
            for row in rows:
                dashboard = Dashboard(
                    stage_id=row["stage_id"],
                    phase_name=row["phase_name"],
                    stage_flag=row["stage_flag"],
                    student_id=row["student_id"],
                )
                dashboards.append(dashboard)

            return dashboards
        finally:
            # 例外の有無に関わらず、最後に必ずクローズする
            cursor.close()
            conn.close()