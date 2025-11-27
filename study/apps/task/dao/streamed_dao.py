# Streamed モデルを MySQL (streamed テーブル) とやり取りする DAO クラス

import mysql.connector
from mysql.connector import MySQLConnection
from models.model_streamed import Streamed
from config.db_config import DB_CONFIG

class StreamedDao:
  """ Streamed テーブルにアクセスするためのDAOクラス """
  
  def __init__(self, config: dict | None = None) -> None:
    # 接続情報を保持（渡されなければ config.DB_CONFIG を使う）
    self.config = config or DB_CONFIG

  def _get_connection(self) -> MySQLConnection:
    """ MySQLとの接続を新しく作成し、返す。 """
    return mysql.connector.connect(**self.config)
  
  # Taskテーブルの利用方法的に違う可能性が高いので、サンプルとして一旦の配置
  def find_all(self) -> list[Streamed]:
    """ 
    streamed テーブルの全レコードを取得
    Streamed オブジェクトのリストとして返す。
    """

    # ここに取得したいSQL文（SELECT）
    sql = """
        SELECT
            streamed.streamed_id,
            streamed.streamed_limit,
            streamed.task_id,
            task.task_text,
            streamed.group_id,
            group.group_name
            
        FROM streamed streamed
        LEFT JOIN task task ON streamed.task_id = task.task_id
        LEFT JOIN group group ON streamed.group_id = group.group_id
        ORDER BY streamed_id ASC
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

      streamed: list[Streamed] = []
      for row in rows:
        stream = Streamed(
          streamed_id=row["streamed_id"],
          streamed_limit=row["streamed_limit"],
          task_id=row["task_id"],
          group_id=row["group_id"]
        )
        streamed.append(stream)

      return streamed
    finally:
      # 例外処理なしで、カーソルと接続を閉じる
      cursor.close()
      conn.close()
          
        
        