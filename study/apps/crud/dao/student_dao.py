import mysql.connector
from mysql.connector import MySQLConnection
from typing import Optional
from apps.crud.models.model_student import Student, StudentToGroupname
from apps.config.db_config import DB_CONFIG

# MySQLに直接アクセスするDAOクラス※studentテーブル専用
class StudentDao:

    # 初期化処理
    def __init__(self, config: dict | None = None) -> None:
        self.config = config or DB_CONFIG

    # DB接続作成処理
    def _get_connection(self) -> MySQLConnection:
        return mysql.connector.connect(**self.config)

    # 全件取得
    def find_all(self) -> list[Student]:
        """ 
        studentテーブルの全レコードを取得
        Studentオブジェクトのリストとして返す。
        """
        sql = """
            SELECT
                student_id,
                student_name,
                password,
                birthday,
                alert,
                group_id
            FROM student
            ORDER BY student_id ASC
        """

        # クラス内部の_get_connection()を使ってMySQL接続を取得
        # 結果を辞書形式で取得
        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            rows = cursor.fetchall()

            students: list[Student] = []
            for row in rows:
                student = Student(
                    student_id=row["student_id"],
                    student_name=row["student_name"],
                    password=row["password"],
                    birthday=row["birthday"],
                    alert=bool(row["alert"]),
                    group_id=row["group_id"]
                )
                students.append(student)

            return students
        finally:
            cursor.close()
            conn.close()

    # 全件取得
    def find_all_groupname(self) -> list[StudentToGroupname]:
        """ 
        studentテーブルの全レコードを取得
        Studentオブジェクトのリストとして返す。
        """
        sql = """
            SELECT
                stu.student_id,
                stu.student_name,
                stu.password,
                stu.birthday,
                stu.alert,
                stu.group_id,
                g.group_name
            FROM student AS stu
            LEFT JOIN `group` AS g
              ON stu.group_id = g.group_id
            ORDER BY student_id ASC
        """

        # クラス内部の_get_connection()を使ってMySQL接続を取得
        # 結果を辞書形式で取得
        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            rows = cursor.fetchall()

            result = []
            for row in rows:
                result.append(StudentToGroupname(
                    student_id=row["student_id"],
                    student_name=row["student_name"],
                    password=row["password"],
                    birthday=row["birthday"],
                    alert=bool(row["alert"]),
                    group_id=row["group_id"],
                    group_name=row["group_name"]
                ))

            return result
        finally:
            cursor.close()
            conn.close()

        # 検索用メソッド
    def search_students(self, search_query: str) -> list[StudentToGroupname]:
        """ 
        student_id, student_name, group_name のいずれかに
        検索キーワードが含まれるレコードを取得する。
        """
        # SQL文: LIKE 演算子を使用して部分一致検索を行う
        sql = """
            SELECT
                stu.student_id,
                stu.student_name,
                stu.password,
                stu.birthday,
                stu.alert,
                stu.group_id,
                g.group_name
            FROM student AS stu
            LEFT JOIN `group` AS g
              ON stu.group_id = g.group_id
            WHERE 
                stu.student_id LIKE %s OR 
                stu.student_name LIKE %s OR 
                g.group_name LIKE %s
            ORDER BY stu.student_id ASC
        """

        # 検索キーワードを % で囲んで部分一致にする
        like_query = f"%{search_query}%"
        params = (like_query, like_query, like_query)

        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            # プリペアドステートメントを使用してSQLインジェクションを防止
            cursor.execute(sql, params)
            rows = cursor.fetchall()

            result = []
            for row in rows:
                result.append(StudentToGroupname(
                    student_id=row["student_id"],
                    student_name=row["student_name"],
                    password=row["password"],
                    birthday=row["birthday"],
                    alert=bool(row["alert"]),
                    group_id=row["group_id"],
                    group_name=row["group_name"]
                ))

            return result
        finally:
            cursor.close()
            conn.close()

    # student ID検索
    def find_by_id(self, student_id: int) -> Optional[dict]:
        """ 
        student_idで student テーブルから1件取得。見つからなければNoneを返す。
        戻り値: 辞書型
        """
        sql = """
            SELECT
                student_id,
                student_name,
                password,
                entry_year,
                birthday,
                entry_date,
                is_alert,
                group_id
            FROM student
            WHERE student_id = %s
            LIMIT 1
        """

        # クラス内部の_get_connection()を使ってMySQL接続を取得
        # 結果を辞書形式で取得
        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (student_id,))
            row = cursor.fetchone()
            return row
        finally:
            cursor.close()
            conn.close()

    # 新規登録
    def insert(self, student_id: int, student_name: str, password: str, entry_year, birthday, is_alert: bool, group_id: int) -> int:
        """
        insert文にて学生を追加
        Student IDは手動設定（または別ロジック算出）を想定して引数で受け取る
        """
        sql = """
            INSERT INTO student
                (student_id, student_name, password, entry_year, birthday, entry_date, is_alert, group_id)
            VALUES
                (%s, %s, %s, %s, %s, NOW(), %s, %s)
        """
        # クラス内部の_get_connection()を使ってMySQL接続を取得
        # 実行＆コミット
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (student_id, student_name, password, entry_year, birthday, is_alert, group_id))
            conn.commit()
            
            return student_id
        
        finally:
            cursor.close()
            conn.close()

    # 指定されたgroup_idに属するstudentを取得し、Studentオブジェクトのリストとして返す
    def find_by_group_id(self, group_id: int) -> list[Student]:
        """
        %s はプレースホルダー
        """
        sql = """
            SELECT
                student_id,
                student_name,
                password,
                entry_year,
                birthday,
                entry_date,
                is_alert,
                group_id
            FROM student
            WHERE group_id = %s
            ORDER BY student_id ASC
        """
        
        # クラス内部の_get_connection()を使ってMySQL接続を取得
        # 結果を辞書形式で取得
        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (group_id,))
            rows = cursor.fetchall()
            
            students: list[Student] = []
            for row in rows:
                student = Student(
                    student_id=row["student_id"],
                    student_name=row["student_name"],
                    password=row["password"],
                    entry_year=row["entry_year"],
                    birthday=row["birthday"],
                    entry_date=row["entry_date"],
                    is_alert=bool(row["is_alert"]),
                    group_id=row["group_id"]
                )
                students.append(student)
            return students
        finally:
            # 例外の有無に関わらず、最後に必ずクローズする
            cursor.close()
            conn.close()