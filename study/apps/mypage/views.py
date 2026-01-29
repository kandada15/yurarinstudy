from flask import Blueprint, render_template, redirect
from flask_login import login_required

# Blueprintの作成
mypage_bp = Blueprint(
  "mypage",
  __name__,
  # 使用するテンプレートフォルダ
  template_folder="templates",
  # 専用の静的ファイル(CSS,JS,画像など)を置くフォルダ
  static_folder="static"
)

@mypage_bp.route("/")
# @login_required
def stu_mypage():
  return render_template("mypage/mypage.html")

@mypage_bp.route("/detail")
def learning_detail():
  return render_template("mypage/learning_pro_dis.html")