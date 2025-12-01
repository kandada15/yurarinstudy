# Submission モデルを MySQL (submission テーブル) とやり取りする DAO クラス

import mysql.connector
from mysql.connector import MySQLConnection
from typing import Optional

from apps.task.models.model_submission import Submission
from apps.config.db_config import DB_CONFIG

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
  

  def find_by_task_student(self, task_id, student_id) -> Optional[dict]:
    """
      task_id * student_id に一致する提出物を1件取得する。
      未提出の場合、falseを返す
      戻り値は dict または None。
        keys: submission_id, answer_text, q_t, submit_flag, submit_date, check_flag, return_flag, task_id, student_id
    """
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
        FROM submission
        WHERE task_id = %s AND student_id = %s
        LIMIT 1    
     """
    
    conn = self._get_connection()
    try:
      # cursor(dictionary=True) にし、SELECT文の結果を辞書型で受け取る
      cursor = conn.cursor(dictionary=True)

      # sqlの実行
      cursor.execute(sql, (task_id, student_id))

      # 受講者/課題の１行を取得
      row = cursor.fetchone()
      return row
    finally:
      # 例外処理なしで、カーソルと接続を閉じる
      cursor.close()
      conn.close()
    


  def insert_submission(self, task_id, student_id, answer_text) -> int | None:
    """
      insert文にて新規の提出を挿入する。
      再提出禁止のため、既に submit_flag=1 の提出が存在する場合は None を返す（失敗）。
        成功時は挿入した submission_id を返す。 
    """

    # 既に提出済みかチェック
    existing_sql = "SELECT submission_id, submit_flag FROM submission WHERE task_id=%s AND student_id=%s LIMIT 1"

    sql = """
        INSERT INTO submission
          (answer_text, q_t, submit_flag, submit_date, checked_flag, returned_flag, task_id, student_id)
        VALUES
          (%s, NULL, 1, NOW(), 0, 0, %s, %s)
    """

    conn = self._get_connection()
    try:
      cursor = conn.cursor(dictionary=True)

      # sqlの実行
      cursor.execute(existing_sql, (answer_text, task_id, student_id))
      existing = cursor.fetchone()
      if existing and existing.get("submit_flag"):
        # 既に提出済み → 再提出不可
        return None
      cursor.close()

      """
      新しくカーソルを立ち上げる。
      挿入時に通常のカーソル（辞書型は不使用）
      """
      cursor = conn.cursor()
      cursor.execute(sql, (answer_text, task_id, student_id))
      # DBへコミットする、submission_idが自動採番された場合のコード
      conn.commit()
      return cursor.lastrowid
    finally:
      # 例外処理なしで閉じる
      cursor.close()
      conn.close()

      

  # def update_submission(self, submission_id, answer_text) -> None:
  #   """ 
  #   提出する前のデータの書き換え
  #   受講者に配信された問題をupdate
  #   """
    
  #   sql = """
  #       UPDATE submission
  #       SET answer_text = %s,
  #           submit_date = NOW(),
  #       WHERE submission_id = %s
  #   """

  #   conn = self._get_connection()
  #   try:
  #     # cursor() にし、辞書型で受け取る必要はない
  #     cursor = conn.cursor()

  #     # sqlの実行
  #     cursor.execute(sql, (answer_text, submission_id))

  #     # DBへコミット
  #     conn.commit()
  #   finally:
  #     cursor.close()
  #     conn.close()
    

          
        
        