import mysql.connector
from mysql.connector import MySQLConnection
from apps.task.models.model_returned import Returned
from apps.config.db_config import DB_CONFIG

# MySQLに直接アクセスするDAOクラス※returnedテーブル専用
class ReturnedDao:
  
  # 初期化処理
  def __init__(self, config: dict | None = None) -> None:
    # 接続情報を保持（渡されなければ config.DB_CONFIG を使う）
    self.config = config or DB_CONFIG

  # DB接続作成処理
  def _get_connection(self) -> MySQLConnection:
    """ MySQLとの接続を新しく作成し、返す。 """
    return mysql.connector.connect(**self.config)
  
  # 全件取得
  def find_all(self) -> list[Returned]:
    """ 
    returned テーブルの全レコードを取得
    Returned オブジェクトのリストとして返す。
    返却済課題情報を返却済課題ID順で取得
    """
    sql = """
        SELECT
            returned_id,
            check_text,
            q_a_t,
            submission_id

        FROM returned
        ORDER BY returned_id ASC
    """

    # クラス内部の_get_connection()を使ってMySQL接続を取得
    # 結果を辞書形式で取得
    conn = self._get_connection()
    try:
      cursor = conn.cursor(dictionary=True)
      cursor.execute(sql)
      rows = cursor.fetchall()

      # Returnedオブジェクトに変換
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
      # 例外の有無に関わらず、最後に必ずクローズする
      cursor.close()
      conn.close()