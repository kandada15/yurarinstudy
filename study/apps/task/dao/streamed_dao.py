import mysql.connector
from mysql.connector import MySQLConnection
from typing import Text
from datetime import datetime


from apps.task.models.model_streamed import Streamed, StreamedForStudent, StreamedForStudentDetail
from apps.config.db_config import DB_CONFIG

# MySQLに直接アクセスするDAOクラス※steamedテーブル専用
class StreamedDao:
  
  # 初期化処理
  def __init__(self, config: dict | None = None) -> None:
    self.config = config or DB_CONFIG

  # DB接続作成処理
  def _get_connection(self) -> MySQLConnection:
    return mysql.connector.connect(**self.config)
  
  # 全件取得
  def find_all(self) -> list[Streamed]:
    """ 
    streamedテーブルの全レコードを取得
    Streamedオブジェクトのリストとして返す。
    配信済課題の情報をstreamed_id順で取得
    """
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

    # クラス内部の_get_connection()を使ってMySQL接続を取得
    # 結果を辞書形式で取得
    conn = self._get_connection()
    try:
      cursor = conn.cursor(dictionary=True)
      cursor.execute(sql)
      rows = cursor.fetchall()

      # Streamedオブジェクトに変換
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
      cursor.close()
      conn.close()

  # streamed新規登録
  def insert(self, streamed_name: str, streamed_text: Text, streamed_limit: datetime, group_id: int):
    """ 
    insert文にて配信済課題を追加 
    streamed_limit は文字列でも DATE 型に変換可能
    """
    sql = """
        INSERT INTO streamed 
          (streamed_name, streamed_text, streamed_limit, group_id)
        VALUES 
          (%s, %s, %s, %s)
    """

    # クラス内部の_get_connection()を使ってMySQL接続を取得
    # 実行＆コミット
    conn = self._get_connection()
    try:
      cursor = conn.cursor()
      cursor.execute(sql, (streamed_name, streamed_text, streamed_limit, group_id))
      # streamed_idが自動採番された場合のコード
      conn.commit()
      return cursor.lastrowid
    
    finally:
      cursor.close()
      conn.close()


  # 受講者『課題一覧画面』用の情報取得
  def find_all_for_student(self) -> list[StreamedForStudent]:
    """
    課題名/配信者/提出期限を表示する
    →groupのcreated_by_admin_nameを持って来る
      ※group作成者=課題作成者
    """
    sql = """
        SELECT
            s.streamed_id,
            s.streamed_name,
            s.streamed_limit,
            admin.admin_name,
            s.sent_at
        FROM streamed AS s
        LEFT OUTER JOIN `group` AS g
          ON s.group_id = g.group_id
        LEFT OUTER JOIN admin 
          ON g.created_by_admin_id = admin.admin_id
        ORDER BY s.sent_at DESC
    """
    # クラス内部の_get_connection()を使ってMySQL接続を取得
    # 結果を辞書形式で取得
    conn = self._get_connection()
    try:
      cursor = conn.cursor(dictionary=True)
      cursor.execute(sql)
      rows = cursor.fetchall()

      # StreamedForStudentオブジェクトに変換
      streamed: list[StreamedForStudent] = []
      for row in rows:
        stream = StreamedForStudent(
          streamed_id=row["streamed_id"],
          streamed_name=row["streamed_name"],
          streamed_limit=row["streamed_limit"],
          admin_name=row["admin_name"],
          sent_at=row["sent_at"]
        )
        streamed.append(stream)

      return streamed
    finally:
      # 例外の有無に関わらず、最後に必ずクローズする
      cursor.close()
      conn.close()

  def find_by_id(self, streamed_id: int) -> StreamedForStudentDetail | None:
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
  def get_streamed_count(self, admin_id: str) -> int:
        """管理者が配信した課題の総数をカウント"""
        sql = """
            SELECT COUNT(*) AS count 
            FROM streamed AS s
            JOIN `group` AS g ON s.group_id = g.group_id
            WHERE g.created_by_admin_id = %s
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (admin_id,))
            row = cursor.fetchone()
            return row["count"] if row else 0
        finally:
            cursor.close()
            conn.close()

  def get_weekly_deadline_count(self) -> int:
      """今日から1週間以内に締切が来る課題の数をカウント"""
      sql = """
          SELECT COUNT(*) AS count 
          FROM streamed 
          WHERE streamed_limit BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 7 DAY)
      """
      conn = self._get_connection()
      try:
          cursor = conn.cursor(dictionary=True)
          cursor.execute(sql)
          row = cursor.fetchone()
          return row["count"] if row else 0
      finally:
          cursor.close()
          conn.close()
=======
            s.streamed_id,
            s.streamed_name,
            s.streamed_text,
            s.streamed_limit,
            admin.admin_name
        FROM streamed AS s
        LEFT OUTER JOIN `group` AS g
          ON s.group_id = g.group_id
        LEFT OUTER JOIN admin 
          ON g.created_by_admin_id = admin.admin_id
        WHERE s.streamed_id = %s
    """
    conn = self._get_connection()
    try:
      # cursor(dictionary=True) にし、SELECT文の結果を辞書型で受け取る
      # row[""],row[""]でアクセス可能
      cursor = conn.cursor(dictionary=True)

      # sqlの実行
      cursor.execute(sql, (streamed_id,))

      # 全行を取得
      row = cursor.fetchone()
      return StreamedForStudentDetail(
        streamed_id=row["streamed_id"],
        streamed_name=row["streamed_name"],
        streamed_text=row["streamed_text"],
        streamed_limit=row["streamed_limit"],
        admin_name=row["admin_name"]
      )
    finally:
      # 例外処理なしで、カーソルと接続を閉じる
      cursor.close()
      conn.close()
