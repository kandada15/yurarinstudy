# Submission モデルを MySQL (submission テーブル) とやり取りする DAO クラス

import mysql.connector
from mysql.connector import MySQLConnection
from models.model_submission import Submission
from config.db_config import DB_CONFIG

class SubmissionDao:
  """ Submission テーブルにアクセスするためのDAOクラス """
  
  def __init__(self, config: dict | None = None) -> None:
    # 接続情報を保持（渡されなければ config.DB_CONFIG を使う）
    self.config = config or DB_CONFIG

  def _get_connection(self) -> MySQLConnection:
    """ MySQLとの接続を新しく作成し、返す。 """
    return mysql.connector.connect(**self.config)
  
  # Taskテーブルの利用方法的に違う可能性が高いので、サンプルとして一旦の配置
  def find_all(self) -> list[Submission]:
    """ 
    submission テーブルの全レコードを取得
    Submission オブジェクトのリストとして返す。
    """

    # ここに取得したいSQL文（SELECT）
    sql = """
        SELECT
            submission_id,
            answer_text,
            q_t,
            submit_flag,
            submit_date,
            checked_flag,
            returned_flag,
            task_id,
            student_id

        FROM submission sub
        ORDER BY submission_id ASC
    """

    conn = self._get_connection()
    try:
      # cursor(dictionary=True) にし、SELECT文の結果を辞書型で受け取る
      # row[""],row[""]でアクセス可能
      cursor = conn.cursor(dictionary=True)

      # sqlの実行
      cursor.execute(sql)

      # 全行を取得
      rows = cursor.fetchall()

      submissions: list[Submission] = []
      for row in rows:
        submission = Submission(
          submission_id=row["submission_id"],
          answer_text=row["answer_text"],
          q_t=row["q_t"],
          submit_flag=row["submit_flag"],
          submit_date=row["submit_date"],
          checked_flag=row["checked_flag"],
          returned_flag=row["returned_flag"],
          task_id=row["task_id"],
          student_id=row["student_id"],
        )
        submissions.append(submission)

      return submissions
    finally:
      # 例外処理なしで、カーソルと接続を閉じる
      cursor.close()
      conn.close()
          
        
        