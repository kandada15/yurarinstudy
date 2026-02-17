import mysql.connector
from mysql.connector import MySQLConnection
from apps.dashboard.models.model_dashboard import Dashboard, StreamedStudent, GroupInStreamed
from apps.config.db_config import DB_CONFIG
import re
# MySQLに直接アクセスするDAOクラス※progressテーブル専用
class Dashboard_DAO:

    # 初期化処理
    def __init__(self, config: dict | None = None) -> None:
        # DB接続情報を受け取る（指定がなければ DB_CONFIG を使う）
        self.config = config or DB_CONFIG

    # DB接続作成処理
    def _get_connection(self) -> MySQLConnection:
        """MySQL への接続を新しく1つ作って返す"""
        return mysql.connector.connect(**self.config)

    # ダッシュボードに表示する統計情報（管理者・グループ・課題状況など）をまとめて取得
    def find_all(self) -> list[Dashboard]:
        """
        progress テーブルの全レコードを取得して、
        Progress オブジェクトのリストとして返す
        ※複数件をまとめて返す
        """
        sql = """
            SELECT
                d.DASHBOARD_ID,
                
                -- 管理者情報
                a.ADMIN_ID,
                a.ADMIN_NAME,
                a.GRROUP_NAME
                
                -- グループ情報
                g.GROUP_NAME,
                g.ADMIN_NAME AS GROUP_ADMIN_NAME,
                
                -- 配信済課題情報
                -- 累計課題配信数
                
                -- 未添削課題数
                
                -- 提出済課題数
                
                -- 未提出課題数
                
                -- 学習進捗(遷移するだけ)
                
                
    
                -- 返却済課題(遷移するだけ)

            FROM DASHBOARD d
            INNER JOIN ADMIN a ON d.ADMIN_ID = a.ADMIN_ID
            INNER JOIN GROUP g ON d.GROUP_ID = g.GROUP_ID
            INNER JOIN PROGRESS p ON d.PROGRESS_ID = p.PROGRESS_ID
            INNER JOIN TASK t ON d.TASK_ID = t.TASK_ID
            OIN SUBMISSION s ON d.SUBMISSION_ID = s.SUBMISSION_ID;
        """

        # クラス内部の_get_connection()を使ってMySQL接続を取得
        # 結果を辞書形式で取得
        conn = self._get_connection()
        try:
            # dictionary=True にすると、結果が dict 形式で返る（列名でアクセスできる）
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            rows = cursor.fetchall()

            # Dashboardオブジェクトに変換
            dashboards: list[Dashboard] = []
            for row in rows:
                dashboard = Dashboard(
                    stage_id=row["stage_id"],
                    phase_name=row["phase_name"],
                    stage_flag=row["stage_flag"],
                    student_id=row["student_id"],
                )
                dashboards.append(dashboard)

            return dashboards
        finally:
            # 例外の有無に関わらず、最後に必ずクローズする
            cursor.close()
            conn.close()

    # 特定の課題について、全学生の提出・添削状況を一覧取得
    def find_students_status_by_streamed_id(
        self, streamed_id: int, admin_id: int, keyword: str | None
    ) -> list[StreamedStudent]:
        """
        指定された課題（streamed_id）について、
        配信された学生と提出・添削状況を取得する（管理者用）
        """
        sql = """
            SELECT
                stu.student_id,
                stu.student_name,
                s.streamed_id,
                g.group_name,
                sub.submission_id,
                sub.submit_flag,
                sub.check_flag
            FROM streamed AS s
            INNER JOIN `group` AS g
                ON g.group_id = s.group_id
            LEFT OUTER JOIN student AS stu
                ON stu.group_id = s.group_id
            LEFT OUTER JOIN submission AS sub
                ON sub.student_id = stu.student_id
            AND sub.streamed_id = s.streamed_id
            WHERE 
                s.streamed_id = %s 
                AND s.group_id
                IN (SELECT group_id FROM `group` WHERE created_by_admin_id = %s)
                AND (%s IS NULL OR stu.student_name LIKE CONCAT('%', %s, '%'))
            ORDER BY stu.student_id ASC
        """

        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (streamed_id, admin_id, keyword, keyword))
            rows = cursor.fetchall()

            result = []
            for row in rows:
                if row["submit_flag"] is None or row["submit_flag"] == 0:
                    status = "未提出"
                elif row["submit_flag"] == 1 and row["check_flag"] == 0:
                    status = "未添削"
                else:
                    status = "添削済み"
                result.append(
                    StreamedStudent(
                        student_id=row["student_id"],
                        student_name=row["student_name"],
                        streamed_id=row["streamed_id"],
                        submission_id=row["submission_id"],
                        status=status,
                        group_name=row["group_name"],
                    )
                )

            return result

        finally:
            cursor.close()
            conn.close()

    # 配信課題IDから、課題のタイトルのみを取得
    def find_streamed_name_by_id(self, streamed_id: int):
        sql = """
        SELECT 
            streamed_name
            FROM streamed
            WHERE streamed_id = %s
        """

        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (streamed_id,))
            row = cursor.fetchone()

            return row
        finally:
            cursor.close()
            conn.close()

    # 提出物IDから、1件の提出情報を取得
    def find_submission_by_id(self, submission_id: int):
        sql = """
        SELECT
            sub.submission_id,
            sub.answer_text,
            sub.submit_flag,
            sub.check_flag,
            sub.return_flag
            FROM submission AS sub
            WHERE sub.submission_id = %s
        """

        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (submission_id,))
            row = cursor.fetchone()

            return row
        finally:
            cursor.close()
            conn.close()

    # 添削画面を表示するために必要な、学生名・課題内容・解答テキストをまとめて取得
    def find_submission_by_streamed_id(self, submission_id: int, admin_id: int):
        """
        指定された課題に続いて、受講者が解答した解答を取得し
        添削を行う。学生名や課題タイトル、フラグを取得する。
        →添削画面を表示する
        """
        sql = """
            SELECT
                sub.submission_id,
                sub.answer_text,
                sub.check_flag,
                s.streamed_id,
                s.streamed_name,
                s.streamed_text,
                stu.student_name
            FROM submission AS sub
            INNER JOIN streamed AS s
            ON sub.streamed_id = s.streamed_id
            INNER JOIN student AS stu
            ON sub.student_id = stu.student_id
            INNER JOIN `group` AS g
            ON stu.group_id = g.group_id
            WHERE sub.submission_id = %s 
            AND g.created_by_admin_id = %s 
            ORDER BY stu.student_id ASC
        """

        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (submission_id, admin_id))
            row = cursor.fetchone()
            return row

        finally:
            cursor.close()
            conn.close()

    # 添削完了時、提出物テーブルの添削フラグを「済み」に更新
    def update_submission_correction(self, submission_id: int):
        """
        添削結果を保存し、check_flag を ON にする
        """
        sql = """
            UPDATE submission
            SET
            check_flag = 1,
            submitted_at = NOW()
            WHERE submission_id = %s
        """

        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (submission_id,))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    # 添削した内容を返却用テーブルに保存
    def insert_returned(self, submission_id: int, check_text: str):
        sql = """
            INSERT INTO returned(
                submission_id,
                check_text,
                returned_at
            )
            VALUES (%s, %s, NOW())
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (submission_id, check_text))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    # その課題に「提出済みだけど、まだ添削されていない人」が残っているか確認
    def exists_unchecked_submission(self, streamed_id: int):
        """
        提出済みかつ未添削課題があれば、エラーメッセージを出す
        """
        sql = """
            SELECT COUNT(*) AS cnt
                FROM submission
                WHERE streamed_id = %s
                AND submit_flag = 1
                AND check_flag = 0
            """
        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (streamed_id,))
            row = cursor.fetchone()
            return row["cnt"] > 0
        finally:
            cursor.close()
            conn.close()

    # その課題に「未提出」または「未添削」の人が1人でもいるか確認
    def exists_flag_check(self, streamed_id: int) -> bool:
        """
        未提出 or 未添削の submission が1件でもあれば 返却不可とする
        """
        sql = """
        SELECT 1
        FROM streamed AS s
        INNER JOIN `group` AS g
        ON g.group_id = s.group_id
        INNER JOIN student AS stu
        ON stu.group_id = g.group_id
        LEFT OUTER JOIN submission AS sub
        ON sub.student_id = stu.student_id
        AND sub.streamed_id = s.streamed_id
        WHERE s.streamed_id = %s
        AND (
            sub.submission_id IS NULL   
            OR sub.submit_flag = 0      
            OR sub.check_flag = 0       
            )
        LIMIT 1
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (streamed_id,))
            row = cursor.fetchone() is not None
            return row
        finally:
            cursor.close()
            conn.close()

    # その課題の全学生に対し、一括で返却フラグを「済み」にする
    def update_return_flag(self, streamed_id: int):
        sql = """
        UPDATE submission
        SET return_flag = 1
        WHERE streamed_id = %s
        AND submit_flag = 1
        AND check_flag = 1
        """

        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (streamed_id,))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    # 管理者が担当するグループの中で、既に返却済みの課題があるグループの一覧を取得
    def find_returned_groups(self, admin_id: int):
        sql = """
            SELECT DISTINCT
                g.group_id,
                g.group_name,
                s.streamed_id,
                s.streamed_name
            FROM submission AS sub
            INNER JOIN streamed AS s
                ON sub.streamed_id = s.streamed_id
            INNER JOIN `group` AS g
                ON s.group_id = g.group_id
            WHERE sub.check_flag = 1
                AND sub.return_flag = 1
                AND g.created_by_admin_id = %s
            ORDER BY s.streamed_id DESC
        """

        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (admin_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    # 特定のグループ・課題において、返却まで完了している学生の一覧を取得
    def find_returned_students_by_group(self, group_id: int, streamed_id: int):
        """
        指定グループ内で
        添削済み＆返却済みの課題を持つ学生のみ取得
        """
        sql = """
            SELECT DISTINCT
                stu.student_id,
                stu.student_name
            FROM submission AS sub
            INNER JOIN student AS stu
                ON sub.student_id = stu.student_id
            INNER JOIN streamed AS s
                ON sub.streamed_id = s.streamed_id
            WHERE s.group_id = %s
                AND s.streamed_id = %s
                AND sub.check_flag = 1
                AND sub.return_flag = 1
            ORDER BY stu.student_id ASC
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                sql,
                (
                    group_id,
                    streamed_id,
                ),
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    # IDまたは名前で学生を絞り込み検索
    def search_by_id_name(self, group_id: int, streamed_id: int, keyword):
        sql = """
            SELECT DISTINCT
                s.student_id,
                s.student_name
            FROM student s
            JOIN submission sub
            ON sub.student_id = s.student_id
            WHERE s.group_id = %s
            AND sub.streamed_id = %s
        """
        params = [group_id, streamed_id]
        # 検索キーワードがある場合のみ条件を追加
        if keyword:
            sql += """
            AND (
                s.student_id LIKE %s
                OR s.student_name LIKE %s
            )
        """
            like_keyword = f"%{keyword}%"
            params.extend([like_keyword, like_keyword])

        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, params)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    # 返却済み課題の一覧画面を表示するために必要な、課題とグループの情報を取得
    def find_by_group_for_submission(self) -> list[GroupInStreamed]:
        """
        返却済み課題一覧を得るために必要なカラム
        フラグ=返却済みが立っている学生を絞込み
        ・返却済み（check_flag=1）
        ・課題
        ・グループ
        ・学生
        """
        sql = """
            SELECT DISTINCT
                s.streamed_id,
                s.streamed_name,
                g.group_id,
                g.group_name
            FROM submission AS sub
            INNER JOIN streamed AS s
                ON sub.streamed_id = s.streamed_id
            INNER JOIN `group` AS g
                ON s.group_id = g.group_id
            WHERE sub.check_flag = 1
                AND sub.return_flag = 1
            ORDER BY g.group_id ASC
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            rows = cursor.fetchall()

            returned: list[GroupInStreamed] = []
            for row in rows:
                gis = GroupInStreamed(
                    streamed_id=row["streamed_id"],
                    streamed_name=row["streamed_name"],
                    group_id=row["group_id"],
                    group_name=row["group_name"],
                )
                returned.append(gis)

            return returned
        finally:
            cursor.close()
            conn.close()

    # 学生側から見て、自分に「返却（添削完了）」された課題の一覧をすべて取得
    def find_returned_tasks_by_student(self, student_id: int):
        """
        返却済み課題の一覧を取得
        return_flag = 1
        """
        sql = """
            SELECT
                s.streamed_id,
                s.streamed_name,
                s.sent_at,
                g.group_name,
                s.streamed_limit,
                admin.admin_name,
                stu.student_name,
                sub.submission_id
            FROM streamed AS s
            INNER JOIN `group` AS g ON s.group_id = g.group_id
            INNER JOIN admin ON g.created_by_admin_id = admin.admin_id 
            INNER JOIN student AS stu ON stu.student_id = %s
            LEFT JOIN submission AS sub ON s.streamed_id = sub.streamed_id AND sub.student_id = %s
            WHERE sub.student_id = %s
                AND sub.check_flag = 1
                AND sub.return_flag = 1
            ORDER BY s.sent_at DESC
        """
            
        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (student_id, student_id, student_id))
            result = cursor.fetchall()
            return result
        finally:
            cursor.close()
            conn.close()
    
    # 文字列からHTMLタグ（<p>など）を取り除き、純粋なテキストのみにする
    def strip_tags(self, text: str | None) -> str:
        if not text:
            return ""
        return re.sub(r"<[^>]*?>", "", text)
