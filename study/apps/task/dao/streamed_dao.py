# Streamed モデルを MySQL (streamed テーブル) とやり取りする DAO クラス

import mysql.connector
from mysql.connector import MySQLConnection
from apps.task.models.model_streamed import Streamed
from apps.task.models.model_task import Task
from apps.config.db_config import DB_CONFIG

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
            s.streamed_id,
            s.streamed_limit,
            s.task_id,
            t.task_text,
            s.group_id,
            g.group_name
            
        FROM streamed AS s
        LEFT JOIN task AS t ON s.task_id = t.task_id
        LEFT JOIN `group` AS g ON s.group_id = g.group_id
        ORDER BY s.streamed_id ASC
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
          group_id=row["group_id"],
          task_text=row.get("task_text"),
          group_name=row.get("group_name")
          
        )
        streamed.append(stream)

      return streamed
    finally:
      # 例外処理なしで、カーソルと接続を閉じる
      cursor.close()
      conn.close()

  def find_by_group(self, group_id: int) -> list:
    """
    group_idを探すための関数を設定
    """

    sql = """
        SELECT
        st.task_id,
        st.group_id,
        st.streamed_limit,
        t.task_name,
        t.task_text

        FROM streamed AS st
        INNER JOIN task AS t ON st.task_id = t.task_id
        WHERE ts.group_id = %s
        ORDER BY st.streamed_limit ASC
    """

    conn = self._get_connection()
    try:
      # cursor(dictionary=True) にし、SELECT文の結果を辞書型で受け取る
      # row[""],row[""]でアクセス可能
      cursor = conn.cursor(dictionary=True)

      # sqlの実行
      cursor.execute(sql, (group_id))

      # 全行を取得
      rows = cursor.fetchall()

      # 新たにtasksリストを生成、提出状況を追加
      tasks = []
      for row in rows:
        task = Task(
          task_id=row["task_id"],
          task_name=row["task_name"],
          task_text=row["task_text"],
          submit_limit=row["submit_limit"]
        )
        tasks.append(task)

      return tasks
    finally:
      # 例外処理なしで、カーソルと接続を閉じる
      cursor.close()
      conn.close()



  def insert(self, streamed_limit, task_id, group_id):
    sql = """
        INSERT INTO streamed 
          (streamed_limit, task_id, group_id)
        VALUES 
          (NOW(), %s, %s)
    """

    conn = self._get_connection()
    try:
      # cursor() にする。辞書型にする必要はないため。
      cursor = conn.cursor()

      # sqlの実行
      cursor.execute(sql, (task_id, group_id, streamed_limit))

      # DBへコミットする、streamed_idが自動採番された場合のコード
      conn.commit()
      return cursor.lastrowid
    
    finally:
      # 例外処理なしで閉じる
      cursor.close()
      conn.close()



          
        
        