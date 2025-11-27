# Task モデルを MySQL (task テーブル) とやり取りする DAO クラス

import mysql.connector
from mysql.connector import MySQLConnection
from apps.task.models.model_task import Task
from apps.config.db_config import DB_CONFIG

class TaskDao:
  """ TaskテーブルにアクセスするためのDAOクラス """
  
  def __init__(self, config: dict | None = None) -> None:
    # 接続情報を保持（渡されなければ config.DB_CONFIG を使う）
    self.config = config or DB_CONFIG

  def _get_connection(self) -> MySQLConnection:
    """ MySQLとの接続を新しく作成し、返す。 """
    return mysql.connector.connect(**self.config)
  
  # Taskテーブルの利用方法的に違う可能性が高いので、サンプルとして一旦の配置
  def find_all(self) -> list[Task]:
    """ 
    taskテーブルの全レコードを取得
    Taskオブジェクトのリストとして返す。
    """
    # ここに取得したいSQL文（SELECT）
    sql = """
        SELECT
            task_id,
            task_name,
            task_text
            
        FROM task
        ORDER BY task_id ASC
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

      tasks: list[Task] = []
      for row in rows:
        task = Task(
          task_id=row["task_id"],
          task_name=row["task_name"],
          task_text=row["task_text"]
        )
        tasks.append(task)

      return tasks
    finally:
      # 例外処理なしで、カーソルと接続を閉じる
      cursor.close()
      conn.close()
          
        
        