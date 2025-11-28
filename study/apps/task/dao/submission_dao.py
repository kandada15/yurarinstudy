# Submission モデルを MySQL (submission テーブル) とやり取りする DAO クラス

import mysql.connector
from mysql.connector import MySQLConnection
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
  

  def find_by_task_student(self, task_id, student_id) -> Submission | None:
    """
      一つの課題に対して、一人の受講者の提出状況を取得する
      未提出の場合、falseを返す
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
      # row[""],row[""]でアクセス可能
      cursor = conn.cursor(dictionary=True)

      # sqlの実行
      cursor.execute(sql, (task_id, student_id))

      # 受講者/課題の１行を取得
      row = cursor.fetchone()

      if row is None:
        return None

      return Submission(
          submission_id=row["submission_id"],
          answer_text=row["answer_text"],
          q_t=row["q_t"],
          submit_flag=row["submit_flag"],
          submit_date=row["submit_date"],
          checked_flag=row["checked_flag"],
          returned_flag=row["returned_flag"],
          task_id=row["task_id"],
          student_id=row["student_id"]
        )

    finally:
      # 例外処理なしで、カーソルと接続を閉じる
      cursor.close()
      conn.close()
    



    
  def insert(self, task_id, student_id, answer_text) -> int:
    """
      insert文にて新しいデータを追加する役割
      VALUESにて値を設定 
    """

    sql = """
        INSERT INTO submission
          (answer_text, q_t, submit_flag, submit_date,checked_flag, returned_flag, task_id, student_id)
        VALUES
          (%s, NULL, 1, NOW(), 0, 0, %s, %s)
    """

    conn = self._get_connection()
    try:
      # cursor() にする。辞書型にする必要はないため。
      cursor = conn.cursor()

      # sqlの実行
      cursor.execute(sql, (answer_text, task_id, student_id))

      # DBへコミットする、submission_idが自動採番された場合のコード
      conn.commit()
      return cursor.lastrowid
    
    finally:
      # 例外処理なしで閉じる
      cursor.close()
      conn.close()

      

  def update_submission(self, submission_id, answer_text) -> None:
    """ 
    提出する前のデータの書き換え
    受講者に配信された問題をupdate
    """
    
    sql = """
        UPDATE submission
        SET answer_text = %s,
            submit_date = NOW(),
        WHERE submission_id = %s
    """

    conn = self._get_connection()
    try:
      # cursor() にし、辞書型で受け取る必要はない
      cursor = conn.cursor()

      # sqlの実行
      cursor.execute(sql, (answer_text, submission_id))

      # DBへコミット
      conn.commit()
    finally:
      cursor.close()
      conn.close()
    

          
        
        