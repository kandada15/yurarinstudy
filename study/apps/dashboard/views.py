from flask import Blueprint, redirect, render_template
from flask_login import login_required

dash_bp = Blueprint(
  'dashboard',
  __name__,
  template_folder='templates',
  static_folder='static'
)

@dash_bp.route('/')
# @login_required
def index():
  # ログイン後、初期画面
  return render_template("dashboard/dashboard.html")

# 配信済みの課題一覧

# 課題ごとの提出状況一覧

# 添削画面の表示