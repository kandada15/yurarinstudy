from flask import Blueprint, render_template
from .dao.task_dao import TaskDao

task_bp = Blueprint(
  "task",
  __name__,
  template_folder="templates",
  static_folder="static"
)

task_dao = TaskDao()

# 課題作成機能
@task_bp.route("/")
def task():
  task_list = task_dao.find_all()
  return render_template('task_admin/ass_create.html', task=task_list)

# 課題配信
@task_bp.route("/stream")
def task_streamed():
  pass

# 課題一覧、内容の表示

# 課題の提出を行う