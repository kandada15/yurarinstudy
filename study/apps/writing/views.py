from flask import Blueprint, render_template

# アプリの作成
writing_bp = Blueprint(

  'writing',
  __name__,
  template_folder='templates',
  static_folder='static',
  url_prefix="/writing"
)


@writing_bp.route('/')

def index():
  """ライティングトップ / カテゴリ一覧ページ"""
  return render_template('index.html')

@writing_bp.route('/step_list')
def step_list():
  """ステージ一覧ページ"""
  return render_template('step_list.html')

@writing_bp.route('/step_learning')
def step_learning():
  """ステージ一覧ページ"""
  return render_template('step_learning.html')

