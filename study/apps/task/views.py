from flask import Blueprint, render_template, request, redirect, url_for, flash
# 以下、11/27作成
from flask_login import login_required, current_user

from .dao.task_dao import TaskDao
from .dao.streamed_dao import StreamedDao
from .dao.submission_dao import SubmissionDao
# 以下、11/27作成時
# from .dao.group_dao import GroupDao


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
# group_dao = GroupDao()

""" 
課題一覧画面→(task_list)一応でおいているだけなので編集必須
task_indexについて：学生用機能として起用、配信日、タイトル、配信者、提出期限
受講者用トップ画面より、「課題一覧」を押下することで関数が動く
streamedDBによりデータを取得後、画面へ表示
"""
@task_bp.route("/")
def task_index():
  task_list = task_dao.find_all()
  return render_template('task_stu/ass_list.html', tasks=task_list)

""" 課題作成画面(入力フォーム) """
@task_bp.route("/create", methods=["GET"])
def task_create_form():
  # 配信先選択用にグループ一覧を取得
  groups = group_dao.find_all()
  return render_template("task_admin/ass_create.html", groups=groups)

""" 課題作成画面(POST) """
# 入力フォーム(GET)より入力した値を受け取って、データを送信する
@task_bp.route("/create", methods=["POST"])
def task_create():
  task_name = request.form.get("task_name")
  task_text = request.form.get("task_text")
  group_id = request.form.get("group_id")
  streamed_limit = request.form.get("streamed_limit")

  # バリデーション
  if not task_name or not task_text or not group_id or not streamed_limit:
    flash("入力内容のいずれかに不備があります。", "error")
    return redirect(url_for("task.task_create_form"))
  
  # Taskを登録
  task_id = task_dao.insert(task_name, task_text)
  
  # 配信テーブルへDB登録
  streamed_dao.insert(task_id=task_id, group_id= group_id, streamed_limit=streamed_limit)
  
  return redirect(url_for("task.task_index"))

""" 課題の配信（課題を選択し、グループと期限を設定）→ (task_stream)一応でおいてるだけ、編集必須 """
@task_bp.route("/stream", methods=["GET"])
def task_stream():
  # 課題とグループの一覧を取得
  tasks = task_dao.find_all()
  groups = group_dao.find_all()

  return render_template("task_admin/task_stream.html", 
                         tasks=tasks, 
                         groups = groups)

""" 課題配信を登録（POST） """
@task_bp.route("/stream", methods=["POST"])
def task_stream_post():
  task_id = request.form.get("task_id")
  group_id = request.form.get("group_id")
  streamed_limit = request.form.get("streamed_limit")

  # 入力チェック
  if not task_id or not group_id or not streamed_limit:
    flash("入力内容のいずれかに不備があります。", "error")
    return redirect(url_for("task.task_stream"))
  
  # DB登録
  streamed_dao.insert(streamed_limit, task_id, group_id)

  # 完了画面は別であるためflashは無し
  return redirect(url_for("task.task_stream"))

""" 
以下、student用機能
login_requiredでログインしていないとは入れないように

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
  for task in tasks:
    submission = submission_dao.find_by_task_student(task_id=task.task_id, student_id=student_id)
    task_status_list.append({
      # 課題情報を格納する
      "task": task,
      # 未提出or提出済み、htmlのfor文で使えないかな？
      "submitted": submission.submit_flag if submission else False,
      "submission_id": submission.submission_id if submission else None,
      "streamed_limit": task.streamed_limit
    })
  
  return render_template("student/ass_list.html", task_status_list=task_status_list)

""" 課題の詳細表示 """
"""  
※
提出状況の取得について、再度取得したいデータについて調べる。daoに記入するコードについても。
提出処理の箇所にもあるので、そこも再度調査。
"""
@task_bp.route("/student/tasks/<int:task_id>", methods=["GET"])
# @login_required
def student_task_detail(task_id):
  student_id = current_user.student_id
  # 課題情報の取得
  task = task_dao.find_by_id(task_id)
  # 提出状況の取得
  submission = submission_dao.find_by_task_student(task_id=task_id, student_id=student_id)

  return render_template("student/ass_inq.html",
                          task=task,
                          submission=submission)

""" 提出処理 """
@task_bp.route("/student/tasks/<int:task_id>/submit", methods=["POST"])
# @login_required
def student_task_submit(task_id):
  student_id = current_user.student_id
  answer_text = request.form.get("answer_text")

  # 既に提出済みの場合
  submission = submission_dao.find_by_task_student(task_id=task_id, student_id=student_id)
  if submission and submission.submit_flag:
    return redirect(url_for("task.student_task_detail", task_id=task_id))
  
  # DB登録、新規の場合・更新の場合。解答分の保存
  if submission:
    submission_dao.update_submission(submission.submission_id, answer_text)
  else:
    submission_dao.insert(task_id=task_id, student_id=student_id, answer_text=answer_text)

  # 提出後、フラグ=True
  flash("課題を提出しました。", "success")
  return redirect(url_for("task.student_task_list"))

