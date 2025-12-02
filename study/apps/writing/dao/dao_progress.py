# dao_progress.py
# Progress モデルを MySQL (progress テーブル) とやり取りする DAO クラス

import mysql.connector
from mysql.connector import MySQLConnection
from models.model_progress import Progress
from config.db_config import DB_CONFIG  # ★ これを追加

# # ※ 本番環境では環境変数や設定ファイルに出すべきですが、
# #    学習用なのでここに直接書いています。
# DB_CONFIG = {
#     "host": "localhost",  # MySQL サーバ（自分のPCなら localhost）
#     "user": "root",  # MySQL のユーザー名（環境に合わせて変更）
#     "password": "20260210",  # ↑ あなたのパスワードに変更してください
#     "database": "study",  # 先ほど作成した DB 名
# }


class Progress_DAO:
    """progress テーブルにアクセスするための DAO クラス"""

    # 初期化メソッド
    def __init__(self, config: dict | None = None) -> None:
        # DB接続情報を受け取る（指定がなければ DB_CONFIG を使う）
        self.config = config or DB_CONFIG

    def _get_connection(self) -> MySQLConnection:
        """MySQL への接続を新しく1つ作って返す"""
        return mysql.connector.connect(**self.config)

    def find_all(self,name,id) -> list[Progress]:
        """
        progress テーブルの全レコードを取得して、
        Progress オブジェクトのリストとして返す
        ※複数件をまとめて返す
        """
        # sql = """
        #     SELECT
        #         CASE 
        #             WHEN stage_flag = 1 THEN '履修済'
        #             ELSE '未履修'
        #         END AS stage_status,
        #     FROM progress;
        #     WHERE phase_nme=? AND student_id=?
        # """
        
        
        sql = f"SELECT CASE WHEN stage_flag = 1 THEN '履修済' ELSE '未履修' END AS stage_status FROM progress WHERE phase_name={name} AND student_id={id};"

        conn = self._get_connection()
        try:
            # dictionary=True にすると、結果が dict 形式で返る（列名でアクセスできる）
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            rows = cursor.fetchall()

            for row in rows:
                
                if row["stage_flag"] == 1:
                    message="履修済"
                else:
                    message="未履修"

            return message
        finally:
            # 例外の有無に関わらず、最後に必ずクローズする
            cursor.close()
            conn.close()