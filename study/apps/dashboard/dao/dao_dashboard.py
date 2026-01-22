# dao_dashboard.py
# Dashboard モデルを MySQL (dashboard テーブル) とやり取りする DAO クラス

import mysql.connector
from mysql.connector import MySQLConnection
from models.model_dashboard import Dashboard
from config.db_config import DB_CONFIG  # ★ これを追加

# MySQLに直接アクセスするDAOクラス※progressテーブル専用
class Dashboard_DAO:
    
    # 初期化処理(DB接続設定)
    def __init__(self, config: dict | None = None) -> None:
        # DB接続情報を受け取る（指定がなければ DB_CONFIG を使う）
        self.config = config or DB_CONFIG

    # DB接続メソッド(共通処理)
    def _get_connection(self) -> MySQLConnection:
        """MySQL への接続を新しく1つ作って返す"""
        return mysql.connector.connect(**self.config)

    # 全件取得
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

        # クラス内部の_get_connection()を使ってMySQL接続を取得
        # 結果を辞書形式で取得
        conn = self._get_connection()
        try:
            # dictionary=True にすると、結果が dict 形式で返る（列名でアクセスできる）
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            rows = cursor.fetchall()

            # Dashboardオブジェクトに変換
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