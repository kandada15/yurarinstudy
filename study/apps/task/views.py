from flask import Blueprint, render_template, request, redirect, url_for, session
from .dao.dao_streamed import StreamedDao
from .dao.dao_submission import SubmissionDao
from apps.crud.dao.dao_student import StudentDao
from apps.crud.dao.dao_group import GroupDao

# Blueprintの作成
task_bp = Blueprint(
    "task",
    __name__,
    # 使用するテンプレートフォルダ
    template_folder="templates",
    # 専用の静的ファイル(CSS,JS,画像など)を置くフォルダ
    static_folder="static",
)

# DAO-インスタンス化
streamed_dao = StreamedDao()
submission_dao = SubmissionDao()
group_dao = GroupDao()
student_dao = StudentDao()

"""admin用"""
# 課題作成画面
@task_bp.route("/create", methods=["GET"])
def task_create_form():

    # 配信先選択用にグループ一覧を取得
    groups = group_dao.find_all()
    
    # 課題作成画面表示
    return render_template(
        "task_admin/task_create.html", groups=groups, stream_data={}, mode="input"
    )


# 確認画面
@task_bp.route("/create", methods=["POST"])
def task_create_confirm():
    # グループ一覧取得
    groups = group_dao.find_all()

    # 入力内容を辞書に登録
    stream_data = {
        "streamed_name": request.form.get("streamed_name"),
        "streamed_text": request.form.get("streamed_text"),
        "streamed_limit": request.form.get("streamed_limit"),
        "group_id": request.form.get("group_id"),
    }

    # バリデーション(必須チェック)
    errors = {}
    if not stream_data["streamed_name"]:
        errors["streamed_name"] = "課題タイトルは必須です。"
    if not stream_data["streamed_text"]:
        errors["streamed_text"] = "問題文は必須です"
    if not stream_data["streamed_limit"]:
        errors["streamed_limit"] = "提出期限は必須です"
    if not stream_data["group_id"]:
        errors["group_id"] = "配信先グループは必須です"
        
    # エラーがあれば入力画面に戻す
    if errors:
        return render_template(
            "task_admin/task_create.html",
            groups=groups,
            stream_data=stream_data,
            errors=errors,
            mode="input",
        )

    # 確認画面で表示する配信先グループ名取得
    group = next(
        (g for g in groups if str(g.group_id) == stream_data["group_id"]), None
    )

    # 確認画面表示
    return render_template(
        "task_admin/task_create.html",
        stream_data=stream_data,
        group_name=group.group_name,
        groups=groups,
        mode="confirm",
    )

# 課題配信完了画面
@task_bp.route("/create/done", methods=["POST"])
def task_create_complete():

    # 配信済課題テーブルに保存
    streamed_id = streamed_dao.insert(
        streamed_name=request.form.get("streamed_name"),
        streamed_text=request.form.get("streamed_text"),
        streamed_limit=request.form.get("streamed_limit"),
        group_id=request.form.get("group_id"),
    )

    # 完了画面表示
    return render_template(
        "task_admin/task_create.html", streamed_id=streamed_id, mode="complete"
    )

"""student用"""
# 課題一覧画面
@task_bp.route("/student/tasks", methods=["GET"])
def student_task_list():
    # セッションからログイン中の受講者IDを取得
    student_id = session.get("user_id")
    # 未提出課題取得
    all_tasks = streamed_dao.find_unsubmitted_for_student(student_id)
    # ページ番号取得
    page = request.args.get("page", 1, type=int)
    # 1ページあたり4件取得
    per_page = 4
    offset = (page - 1) * per_page
    tasks = all_tasks[offset : offset + per_page]
    # 次ページ,前ページの有無を判定
    has_next = len(all_tasks) > offset + per_page
    has_prev = page > 1

    # 表示
    return render_template(
        "task_stu/task_list.html",
        tasks=tasks,
        mode="send",
        page=page,
        has_next=has_next,
        has_prev=has_prev,
    )

# 課題入力画面
@task_bp.route("/student/tasks/<int:streamed_id>/inq", methods=["GET"])
def task_submit(streamed_id):
    task = streamed_dao.find_by_id(streamed_id)
    
    # 入力画面表示
    return render_template("task_stu/task_inq.html", task=task, mode="submit")

# 入力内容保存
@task_bp.route("/student/tasks/<int:streamed_id>/submit", methods=["POST"])
def task_submit_post(streamed_id):
    # 入力内容を取得
    answer_text = request.form.get("answer_text")
    # ログイン中の受講者IDを取得
    student_id = session.get("user_id")
    # 入力内容を提出物テーブルに保存
    submission_dao.insert(
        streamed_id=streamed_id, student_id=student_id, answer_text=answer_text
    )
    
    # 課題一覧画面へリダイレクト
    return redirect(url_for("task.student_task_list"))