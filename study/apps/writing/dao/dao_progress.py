import mysql.connector
from mysql.connector import MySQLConnection
from models.model_progress import Progress
from config.db_config import DB_CONFIG

# MySQLに直接アクセスするDAOクラス※progressテーブル専用
class Progress_DAO:

    # 初期化処理
    def __init__(self, config: dict | None = None) -> None:
        # DB接続情報を受け取る（指定がなければ DB_CONFIG を使う）
        self.config = config or DB_CONFIG

    # DB接続作成処理
    def _get_connection(self) -> MySQLConnection:
        """MySQL への接続を新しく1つ作って返す"""
        return mysql.connector.connect(**self.config)

    # 全件取得
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

        # クラス内部の_get_connection()を使ってMySQL接続を取得
        # 結果を辞書形式で取得
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