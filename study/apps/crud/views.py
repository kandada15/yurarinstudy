from flask import Blueprint, redirect, render_template

# Blueprintの作成
crud_bp = Blueprint(
  'crud',
  __name__,
  # 使用するテンプレートフォルダ
  template_folder='templates',
  # 専用の静的ファイル(CSS,JS,画像など)を置くフォルダ
  static_folder='static'
)

# ルーティングの定義
@crud_bp.route('/')
def index():
  # templates/crud/index.htmlとなる
  return render_template('crud/index.html')