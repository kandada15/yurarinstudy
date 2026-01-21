# Returned モデルを MySQL (returned テーブル) とやり取りする DAO クラス

import mysql.connector
from mysql.connector import MySQLConnection
from apps.task.models.model_returned import Returned
from apps.config.db_config import DB_CONFIG

class ReturnedDao:
  """ Returned テーブルにアクセスするためのDAOクラス """
  
  def __init__(self, config: dict | None = None) -> None:
    # 接続情報を保持（渡されなければ config.DB_CONFIG を使う）
    self.config = config or DB_CONFIG

  def _get_connection(self) -> MySQLConnection:
    """ MySQLとの接続を新しく作成し、返す。 """
    return mysql.connector.connect(**self.config)
  
  # Taskテーブルの利用方法的に違う可能性が高いので、サンプルとして一旦の配置
  def find_all(self) -> list[Returned]:
    """ 
    returned テーブルの全レコードを取得
    Returned オブジェクトのリストとして返す。
    """

    # ここに取得したいSQL文（SELECT）
    sql = """
        SELECT
            returned_id,
            check_text,
            q_a_t,
            submission_id

        FROM returned
        ORDER BY returned_id ASC
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

      returned: list[Returned] = []
      for row in rows:
        one_return = Returned(
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
        returned.append(one_return)

      return returned
    finally:
      # 例外処理なしで、カーソルと接続を閉じる
      cursor.close()
      conn.close()
          
        
        