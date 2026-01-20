# Streamed モデルを MySQL (streamed テーブル) とやり取りする DAO クラス

import mysql.connector
from mysql.connector import MySQLConnection
from typing import List, Text
from datetime import datetime

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
            s.streamed_name,
            s.streamed_text,
            s.streamed_limit,
            g.group_id
            
        FROM streamed AS s
        LEFT OUTER JOIN task AS t ON s.task_id = t.task_id
        LEFT OUTER JOIN `group` AS g ON s.group_id = g.group_id
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
          streamed_name=row["streamed_name"],
          streamed_text=row["streamed_text"],
          streamed_limit=row["streamed_limit"],
          group_id=row["group_id"]
        )
        streamed.append(stream)

      return streamed
    finally:
      # 例外処理なしで、カーソルと接続を閉じる
      cursor.close()
      conn.close()

  
  def insert(self, streamed_name: str, streamed_text: Text, streamed_limit: datetime, group_id: int):
    """ 
    streamed テーブルに配信情報を追加 
    streamed_limit は文字列でも DATE 型に変換可能
    """
    
    sql = """
        INSERT INTO streamed 
          (streamed_name, streamed_text, streamed_limit, group_id)
        VALUES 
          (%s, %s, %s, %s)
    """

    conn = self._get_connection()
    try:
      # cursor() にする。辞書型にする必要はないため。
      cursor = conn.cursor()

      # sqlの実行
      cursor.execute(sql, (streamed_name, streamed_text, streamed_limit, group_id))

      # DBへコミットする、streamed_idが自動採番された場合のコード
      conn.commit()
      return cursor.lastrowid
    
    finally:
      # 例外処理なしで閉じる
      cursor.close()
      conn.close()

  def find_all_for_student(self) -> list[Streamed]:
    sql = """
        SELECT
            streamed_id,
            streamed_name,
            streamed_limit,
            created_by_admin_name,
            sent_at
        FROM streamed
        ORDER BY created_at DESC
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
          streamed_name=row["streamed_name"],
          streamed_limit=row["streamed_limit"],
          created_by_admin_name=row["created_by_admin_name"],
          sent_at=row["sent_at"]
        )
        streamed.append(stream)

      return streamed
    finally:
      # 例外処理なしで、カーソルと接続を閉じる
      cursor.close()
      conn.close()

  def find_by_id(self, streamed_id):
    sql = """
        SELECT
            streamed_id,
            streamed_name,
            streamed_text,
            streamed_limit,
            created_by_admin_name
        FROM streamed
        WHERE streamed_id = %s
    """
    

  """ 関数より持ってきたい情報を明確にしてください """
  def find_by_group(self, group_id) -> List[dict]:
    """
    指定 group_id に配信されている streamed (配信済み課題)を取得する。
    戻り値: list of dict, 各 dict に以下を含む:
          streamed_id, streamed_limit, streamed_date, task_id, task_name, task_text, creator_name (可能なら)
        NOTE: 現在 task テーブルに creator (作成者) カラムが無い場合は creator_name='-' として返す。
    """

    sql = """
        SELECT
        st.streamed_id,
        st.streamed_limit,
        st.sent_at,
        t.task_id,
        t.task_name,
        t.task_text

        FROM streamed AS st
        INNER JOIN task AS t ON st.task_id = t.task_id
        WHERE st.group_id = %s
        ORDER BY st.streamed_limit ASC
    """

    conn = self._get_connection()
    try:
      # cursor(dictionary=True) にし、SELECT文の結果を辞書型で受け取る
      cursor = conn.cursor(dictionary=True)

      # sqlの実行
      cursor.execute(sql, (group_id,))
      rows = cursor.fetchall()

      # 各行に配信者のプレースホルダを含む
      results = []
      for r in rows:
        row = dict(r)
        row.setdefault("creator_name", "-")
        results.append(row)
      return results
    finally:
      cursor.close()
      conn.close()

    #   # 新たにtasksリストを生成、提出状況を追加
    #   tasks = []
    #   for row in rows:
    #     task = Task(
    #       task_id=row["task_id"],
    #       task_name=row["task_name"],
    #       task_text=row["task_text"],
    #       submit_limit=row["submit_limit"]
    #     )
    #     tasks.append(task)

    #   return tasks
    # finally:
    #   # 例外処理なしで、カーソルと接続を閉じる
    #   cursor.close()
    #   conn.close()