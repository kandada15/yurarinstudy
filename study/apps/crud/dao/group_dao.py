import mysql.connector
from mysql.connector import MySQLConnection
from typing import Optional
from apps.crud.models.model_group import Group
from apps.config.db_config import DB_CONFIG

class GroupDao:
    """ groupテーブルにアクセスするためのDAOクラス """

    def __init__(self, config: dict | None = None) -> None:
        self.config = config or DB_CONFIG

    def _get_connection(self) -> MySQLConnection:
        return mysql.connector.connect(**self.config)

    def find_all(self) -> list[Group]:
        """ 
        groupテーブルの全レコードを取得
        Groupオブジェクトのリストとして返す。
        """
        sql = """
            SELECT
                group_id,
                group_name,
                created_by_admin_id
            FROM `group`
            ORDER BY group_id ASC
        """

        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            rows = cursor.fetchall()

            groups: list[Group] = []
            for row in rows:
                group_obj = Group(
                    group_id=row["group_id"],
                    group_name=row["group_name"],
                    admin_id=row["created_by_admin_id"]
                )
                groups.append(group_obj)

            return groups
        finally:
            cursor.close()
            conn.close()

    def find_by_id(self, group_id: int) -> Optional[dict]:
        """ 
        group_idで group テーブルから1件取得。見つからなければNoneを返す。
        戻り値: 辞書型
        """
        sql = """
            SELECT
                group_id,
                group_name,
                created_by_admin_id
            FROM `group`
            WHERE group_id = %s
            LIMIT 1
        """

        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (group_id,))
            row = cursor.fetchone()
            return row
        finally:
            cursor.close()
            conn.close()

    def insert(self, group_name: str, admin_id: str) -> int:
        """
        insert文にてグループを追加
        group_id (AUTO_INCREMENT) を返す
        """
        sql = """
            INSERT INTO `group`
                (group_name, created_by_admin_id)
            VALUES
                (%s, %s)
        """

        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (group_name, admin_id))
            conn.commit()
            
            return cursor.lastrowid
        
        finally:
            cursor.close()
            conn.close()