from flask import Blueprint, render_template  # ← render_template のインポートを追加

# アプリの作成
dashboard_bp = Blueprint(
  "dashboard",
  __name__,
  template_folder="templates",
  static_folder="static"
)

@dashboard_bp.route('/')
def index():
    return render_template('dashboard/dashboard.html')