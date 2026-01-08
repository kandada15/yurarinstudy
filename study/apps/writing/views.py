from flask import Blueprint, render_template
from apps.task.models.model_task import Task
from flask import Blueprint, redirect, render_template, abort

# アプリの作成 (省略なし)
writing_bp = Blueprint(
  'writing',
  __name__,
  template_folder='templates',
  static_folder='static'
)



@writing_bp.route('/')
def index():
  """ライティングトップ / カテゴリ一覧ページ"""
  static_categories = [
        {'task_id': 1, 'task_name': '小論文'},
        {'task_id': 2, 'task_name': 'ビジネス文書'},
        {'task_id': 3, 'task_name': 'レポート'},
        {'task_id': 4, 'task_name': '表現トレーニング'}
    ]
  data = {
        "page_title": "ライティング課題",
        "select_message": "学習したいコンテンツを選択してください",
        "categories": static_categories
    }
  
  return render_template('writing/writing_top.html', data=data)

@writing_bp.route('/step_list')
def step_list():
  """ステージ一覧ページ"""
  return render_template('writing/step_list.html')

@writing_bp.route('/step_learning')
def step_learning():
  """ステージ一覧ページ"""
  return render_template('writing/step_learning.html')