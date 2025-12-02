from flask import Blueprint, render_template, request, redirect, url_for, flash, session
# 以下、11/27作成
from flask_login import login_required, current_user
from datetime import datetime

from .dao.task_dao import TaskDao
from .dao.streamed_dao import StreamedDao
from .dao.submission_dao import SubmissionDao
# 以下、11/27作成時
from apps.crud.dao.group_dao import GroupDao


# アプリの作成
task_bp = Blueprint(
  "task",
  __name__,
  template_folder="templates",
  static_folder="static"
)

""" グループに関することは、後ほど作成！！ """

# DAO-インスタンス化
task_dao = TaskDao()
streamed_dao = StreamedDao()
submission_dao = SubmissionDao()
group_dao = GroupDao()


# @task_bp.route("/")
# def task_index():
#   task_list = task_dao.find_all()
#   return render_template('task_stu/ass_list.html', tasks=task_list)

""" 
課題作成画面(入力フォーム) 
入力項目: 課題名、問題文、提出期限、配信先グループ
"""
@task_bp.route("/create", methods=["GET"])
# @login_required
def task_create_form():
  # 配信先選択用にグループ一覧を取得
  groups = group_dao.find_all()
  return render_template("task_admin/task_create.html", groups=groups)

""" 課題作成画面(POST) """
# 課題作成フォーム(GET)より入力した値を受け取って、確認画面より表示する。
@task_bp.route("/create", methods=["POST"])
# @login_required
def task_create():
  task_name = request.form.get("task_name")
  task_text = request.form.get("task_text")
  group_id = request.form.get("group_id")
  streamed_limit = request.form.get("streamed_limit")

  # バリデーション
  if not task_name or not task_text or not group_id or not streamed_limit:
    flash("入力内容のいずれかに不備があります。", "error")
    return redirect(url_for("task.task_create_form"))
  
  # sessionaに一時保存して確認画面へ渡す。
  task_data = {
    "task_name": task_name, 
    "task_text": task_text,
    "group_id": group_id,
    "streamed_limit": streamed_limit
  }
  session["task_data"] = task_data

  # グループ名を取得,render_templateがなくなったため、取得方法を変える。
  group = next((g for g in group_dao.find_all() if str(g.group_id) == group_id), None)
  
  # Taskを登録
  task_id = task_dao.insert(task_name, task_text)
  
  # 配信テーブルへDB登録
  streamed_dao.insert(task_id=task_id, group_id= group_id, streamed_limit=streamed_limit)

  # 確認画面へ
  return render_template("task_admin/task_create.html", task_data=task_data, task_name=task_name, task_text=task_text, streamed_limit=streamed_limit, group_name=group.group_name)

"""
課題配信の完了。
確認画面で「配信」を押下した際に呼ばれる
DBに課題・配信情報を登録する
"""
@task_bp.route("/create/done", methods=["POST"])
# @login_required
def task_create_complete():
  task_data = session.get('task_data')
  if not task_data:
    flash("課題データが存在しません。再入力してください。", "error")
    return redirect(url_for("task.task_create_form"))
  
  # DBに課題を登録
  task_id = task_dao.insert(task_data["task_name"], task_data["task_text"])

  # 配信日時を現在日時で取得
  streamed_date = datetime.now()

  # 配信済みテーブルに登録
  streamed_dao.insert(
    streamed_limit=task_data["streamed_limit"],
    task_id=task_id,
    group_id=task_data["group_id"],
    streamed_date=streamed_date
  )

  # sessionのデータは削除
  session.pop('task_data', None)

  return render_template(
    "task_admin/task_create.html", task_name=task_data["task_name"], streamed_limit=task_data["streamed_limit"], group_id=task_data["group_id"]
  )



# """ 課題の配信（課題を選択し、グループと期限を設定）→ (task_stream)一応でおいてるだけ、編集必須 """
# @task_bp.route("/stream", methods=["GET"])
# def task_stream():
#   # 課題とグループの一覧を取得
#   tasks = task_dao.find_all()
#   groups = group_dao.find_all()

#   return render_template("task_admin/task_stream.html", 
#                          tasks=tasks, 
#                          groups = groups)

# """ 課題配信を登録（POST） """
# @task_bp.route("/stream", methods=["POST"])
# def task_stream_post():
#   task_id = request.form.get("task_id")
#   group_id = request.form.get("group_id")
#   streamed_limit = request.form.get("streamed_limit")

#   # 入力チェック
#   if not task_id or not group_id or not streamed_limit:
#     flash("入力内容のいずれかに不備があります。", "error")
#     return redirect(url_for("task.task_stream"))
  
#   # DB登録
#   streamed_dao.insert(streamed_limit, task_id, group_id)

#   # 完了画面は別であるためflashは無し
#   return redirect(url_for("task.task_stream"))

""" 
以下、student用機能
login_requiredでログインしていないと入れないようになっている。

課題一覧画面→(task_list)一応でおいているだけなので編集必須
task_indexについて：学生用機能として起用、配信日（？）、タイトル、配信者、提出期限→管理者IDはグループテーブルよりfkで入っている
受講者用トップ画面より、「課題一覧」を押下することで関数が動く
streamedDBによりデータを取得後、画面へ表示
"""

""" 課題一覧の表示 """
@task_bp.route("/student/tasks")
# @login_required
def student_task_list():
  student_id = current_user.student_id
  # current_userのグループIDの取得
  group_id = current_user.group_id

  # current_userに配信されている課題一覧、配信済みテーブルより取得
  ## 「group_id = 」にて指定したcurrent_userより入手したgroup_idと関連付ける
  """ 管理者を取ってくるものが記入されていない。＝配信者を持ってこれない """
  tasks = streamed_dao.find_by_group(group_id)

  # 各課題の提出状況の取得、task_id,task_name,task_text
  task_status_list = []
  for dict_task in tasks:
    submission = submission_dao.find_by_task_student(task_id=dict_task.task_id, student_id=student_id)
    task_status_list.append({
      # dict情報を格納する
      "task": dict_task,
      # 未提出or提出済み
      # "submitted": submission.submit_flag if submission else False,
      "submitted": bool(submission["submit_flag"]) if submission else False,
      "submission_id": submission["submission_id"] if submission else None,
      "streamed_limit": dict_task.get("streamed_limit"),
      "streamed_date": dict_task.get("streamed_date"),
      "creator": dict_task.get("creator_name", "-")
    })
  
  return render_template("student/ass_list.html", task_status_list=task_status_list)


"""  
※
提出状況の取得について、再度取得したいデータについて調べる。daoに記入するコードについても。
提出処理の箇所にもあるので、そこも再度調査。
methods=["GET"]が必要ないかも
"""

""" 課題の詳細表示 """
@task_bp.route("/student/tasks/<int:task_id>")
# @login_required
def student_task_detail(task_id):
  student_id = current_user.student_id
  # 課題情報の取得
  task = task_dao.find_by_id(task_id)

  # 課題が無い場合
  if not task:
    flash("該当する課題が見つかりません", "warning")
    return redirect(url_for("task.student_task_list"))
  
  # 提出状況の取得
  submission = submission_dao.find_by_task_student(task_id=task_id, student_id=student_id)
  return render_template("student/ass_inq.html",
                          task=task,
                          submission=submission)

""" 課題入力画面(入力フォーム) """
@task_bp.route("/student/tasks/<int:task_id>/answer", methods=["GET"])
# @login_required
def student_answer_form(task_id):
  student_id = current_user.student_id
  task = task_dao.find_by_id(task_id)

  if not task:
    flash("該当する課題が見つかりません", "warning")
    return redirect(url_for("task.student_task_list"))
  
  # GET,課題を既に提出済みの場合
  submission = submission_dao.find_by_task_student(task_id=task_id, student_id=student_id)
  if submission and submission.get("submit_flag"):
    flash("この課題は既に提出済みです。", "warning")
    return redirect(url_for("task.student_task_detail", task_id=task_id))
  
  # フォームを表示
  # 以前の解答が存在する場合は事前入力
  exiting_answer = submission.get("answer_text") if submission else ""
  return render_template("student/answer_form.html", task=task, answer_text=exiting_answer)


""" 課題の確認画面 """
@task_bp.route("/student/tasks/<int:task_id>/confirm", methods=["POST"])
# @login_required
def student_answer_confirm(task_id):
  student_id = current_user.student_id
  answer_text = request.form.get("answer_text", "").strip()

  # 解答文が未入力の場合
  if not answer_text:
    flash("入力内容に不備があります。", "warning")
    return redirect(url_for("task.student_answer_form", task_id=task_id))
  
  # 課題が見つからない場合
  task = task_dao.find_by_id(task_id)
  if not task:
    flash("課題が見つかりません。", "warning")
    return redirect(url_for("task.student_task_list"))
  
  # 確認ページの表示
  return render_template("student/answer_confirm.html", task=task, answer_text=answer_text, student_id=student_id)


""" 提出処理 """
@task_bp.route("/student/tasks/<int:task_id>/submit", methods=["POST"])
# @login_required
def student_task_submit(task_id):
  student_id = current_user.student_id
  answer_text = request.form.get("answer_text", "").strip()

  # 既に提出済みの場合
  existing = submission_dao.find_by_task_student(task_id=task_id, student_id=student_id)
  if existing and existing.get("submit_flag"):
    return redirect(url_for("task.student_task_detail", task_id=task_id))
  
  # 既に提出をしていた場合：
  inserted = submission_dao.insert_submission(task_id=task_id, student_id=student_id, answer_text=answer_text)
  if not inserted:
    # 既に送信済みな場合
    return render_template("student/already_submitted.html", task_id=task_id)
  
  # まだ提出をしていない場合
  return render_template("student/answer_complete.html", task_id=task_id)

  # # 提出後、フラグ=True
  # flash("課題を提出しました。", "success")
  # return redirect(url_for("task.student_task_list"))

