import mysql.connector
from mysql.connector import MySQLConnection
from apps.task.models.model_submission import Submission
from apps.config.db_config import DB_CONFIG

# MySQLに直接アクセスするDAOクラス※submissionテーブル専用
class SubmissionDao:

    # 初期化処理
    def __init__(self, config: dict | None = None) -> None:
        self.config = config or DB_CONFIG

    # DB接続作成処理
    def _get_connection(self) -> MySQLConnection:
        return mysql.connector.connect(**self.config)

    # 全件取得
    def find_all(self) -> list[Submission]:
        """
        submissionテーブルの全レコードを取得
        Submissionオブジェクトのリストとして返す。
        提出物情報をsubmission_id順で取得
        """
        sql = """
            SELECT
                submission_id,
                answer_text,
                q_t,
                submit_flag,
                submitted_at,
                checked_flag,
                returned_flag,
                task_id,
                student_id
            FROM submission sub
            ORDER BY submission_id ASC
        """

        # クラス内部の_get_connection()を使ってMySQL接続を取得
        # 結果を辞書形式で取得
        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            rows = cursor.fetchall()

            # Submissionオブジェクトに変換
            submissions: list[Submission] = []
            for row in rows:
                submission = Submission(
                    submission_id=row["submission_id"],
                    answer_text=row["answer_text"],
                    q_t=row["q_t"],
                    submit_flag=row["submit_flag"],
                    submitted_at=row["submitted_at"],
                    checked_flag=row["checked_flag"],
                    returned_flag=row["returned_flag"],
                    task_id=row["task_id"],
                    student_id=row["student_id"],
                )
                submissions.append(submission)

            return submissions
        
        finally:
            # 例外の有無に関わらず、最後に必ずクローズする
            cursor.close()
            conn.close()

    # submission新規登録
    def insert(self, streamed_id, student_id, answer_text):
        """
        insert文にて提出物を追加
        再提出禁止のため、既に submit_flag=1 の提出物が存在する(既存)場合は None を返す
        既存でなければsqlを実行してinsert
        """

        # 提出済かチェック(submit_flag)
        existing_sql = "SELECT submission_id, submit_flag FROM submission WHERE streamed_id=%s AND student_id=%s LIMIT 1"

        sql = """
            INSERT INTO submission
            (streamed_id, student_id, answer_text, submit_flag)
            VALUES
            (%s, %s, %s, 1)
        """

        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)

            # sqlの実行
            cursor.execute(existing_sql, (streamed_id, student_id))
            existing = cursor.fetchone()
            cursor.close()

            # 提出物登録済 → 再提出不可
            if existing and existing.get("submit_flag") == 1:
                return None
            """
            新しくカーソルを立ち上げる。
            挿入時に通常のカーソル（辞書型は不使用）
            """
            # 実行＆コミット
            cursor = conn.cursor()
            cursor.execute(sql, (streamed_id, student_id, answer_text,))
            conn.commit()
            
            return cursor.lastrowid

        finally:
            # 例外の有無に関わらず、最後に必ずクローズする
            cursor.close()
            conn.close()

class SubmissionDao2:
    
    # 初期化処理
    def __init__(self, config=None):
        self.config = config or DB_CONFIG

    # DB接続作成処理
    def _get_connection(self):
        return mysql.connector.connect(**self.config)

    def get_stats(self):
        """提出済課題数と未添削課題数を取得"""
        sql = """
            SELECT 
                COUNT(*) AS submitted_count,
                SUM(CASE WHEN check_flag = 0 THEN 1 ELSE 0 END) AS unchecked_count
            FROM submission
        """
        
        # クラス内部の_get_connection()を使ってMySQL接続を取得
        # 結果を辞書形式で取得
        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            row = cursor.fetchone()
            
            return {
                "submitted_count": row["submitted_count"] if row else 0,
                "unchecked_count": row["unchecked_count"] if row else 0
            }
            
        finally:
            # 例外の有無に関わらず、最後に必ずクローズする
            cursor.close()
            conn.close()