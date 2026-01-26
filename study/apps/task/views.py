from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from .dao.streamed_dao import StreamedDao
from .dao.submission_dao import SubmissionDao
from apps.crud.dao.student_dao import StudentDao
from apps.crud.dao.group_dao import GroupDao


# Blueprintの作成
task_bp = Blueprint(
  "task",
  __name__,
  # 使用するテンプレートフォルダ
  template_folder="templates",
  # 専用の静的ファイル(CSS,JS,画像など)を置くフォルダ
  static_folder="static"
)

# DAO-インスタンス化
streamed_dao = StreamedDao()
submission_dao = SubmissionDao()
group_dao = GroupDao()
student_dao = StudentDao()


""" 
以下、admin用機能
画面: 課題作成画面(入力フォーム) →確認画面→完了画面
入力項目: 課題名、問題文、提出期限、配信先グループ
"""

""" 課題作成画面(GET) """
@task_bp.route("/create", methods=["GET"])
# @login_required
def task_create_form():
  # 配信先選択用にグループ一覧を取得
  groups = group_dao.find_all()
  return render_template("task_admin/task_create.html", groups=groups, stream_data={}, mode="input")

""" 課題作成画面(POST) """
# 課題作成フォーム(GET)より入力した値を受け取って、確認画面より表示する。
@task_bp.route("/create", methods=["POST"])
# @login_required
def task_create_confirm():
  groups = group_dao.find_all()

  # stream_dataにデータを格納する。
  stream_data = {
    "streamed_name": request.form.get("streamed_name"), 
    "streamed_text": request.form.get("streamed_text"),
    "streamed_limit": request.form.get("streamed_limit"),
    "group_id": request.form.get("group_id")
  }

  # バリデーション、エラーメッセージを出力する
  errors = {}

  if not stream_data["streamed_name"]:
    errors["streamed_name"] = "課題タイトルは必須です。"
  if not stream_data["streamed_text"]:
    errors["streamed_text"] = "問題文は必須です"
  if not stream_data["streamed_limit"]:
    errors["streamed_limit"] = "提出期限は必須です"
  if not stream_data["group_id"]:
    errors["group_id"] = "配信先グループは必須です"

  if errors:
    return render_template("task_admin/task_create.html", groups=groups, stream_data=stream_data, errors=errors, mode="input")

  # グループ名を取得する
  group = next((g for g in groups if str(g.group_id) == stream_data["group_id"]), None)

  # 確認画面へ
  return render_template("task_admin/task_create.html", stream_data=stream_data, group_name=group.group_name, groups=groups, mode="confirm")

""" 課題配信の完了画面(POST) """
@task_bp.route("/create/done", methods=["POST"])
# @login_required
def task_create_complete():
  
  # 配信済みテーブルに登録
  streamed_id = streamed_dao.insert(
    streamed_name=request.form.get("streamed_name"),
    streamed_text=request.form.get("streamed_text"),
    streamed_limit=request.form.get("streamed_limit"),
    group_id=request.form.get("group_id")
  )

  return render_template(
    "task_admin/task_create.html", streamed_id=streamed_id, mode="complete")


""" 
以下、student用機能
画面: 配信済み課題一覧の表示画面→(詳細まではjsより表示)→解答入力画面(確認画面はjsより表示)
入力項目: 課題タイトル、問題文、解答文
"""

""" 課題一覧の表示 """
@task_bp.route("/student/tasks", methods=["GET"])
# @login_required
def student_task_list():
  """ 現在ログイン済みの学生のIDと、その学生の未提出課題情報を取得 """
  student_id = session.get('user_id')
  all_tasks = streamed_dao.find_unsubmitted_for_student(student_id)
  # ページネーションの設定
  page = request.args.get('page', 1, type=int)
  per_page = 4 # 1ページあたりの表示件数
  offset = (page - 1) * per_page

  # DAOにoffsetとlimitを渡して取得するように変更
  # 簡易的なページネーション処理
  tasks = all_tasks[offset : offset + per_page]

  # 次のページがあるかどうかの判定
  has_next = len(all_tasks) > offset + per_page
  has_prev = page > 1
  return render_template("task_stu/task_list.html", tasks=tasks, mode="send", page=page, has_next=has_next, has_prev=has_prev)

""" 課題入力画面の表示 """
@task_bp.route("/student/tasks/<int:streamed_id>/inq", methods=["GET"])
# @login_required
def task_submit(streamed_id):
  task = streamed_dao.find_by_id(streamed_id)
  return render_template("task_stu/task_inq.html", task=task, mode="submit")

""" GETより受け取ったデータをINSERT→課題一覧へ戻る """
@task_bp.route("/student/tasks/<int:streamed_id>/submit", methods=["POST"])
def task_submit_post(streamed_id):
  answer_text = request.form.get("answer_text")
  student_id = session.get('user_id')

  submission_dao.insert(
    streamed_id=streamed_id,
    student_id=student_id,
    answer_text=answer_text
  )

  return redirect(url_for("task.student_task_list"))