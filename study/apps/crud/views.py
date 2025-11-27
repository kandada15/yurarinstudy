from flask import Blueprint, redirect, render_template

# アプリの作成
crud_bp = Blueprint(
  'crud',
  __name__,
  # 使用するフォルダ
  template_folder='templates',
  static_folder='static'
)

@crud_bp.route('/')
def index():
  # templates/crud/index.htmlとなる
  return render_template('crud/index.html')