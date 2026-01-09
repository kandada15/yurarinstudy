from apps.task.models.model_task import Task
from flask import Blueprint, redirect, render_template, abort, request

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
    category_id = request.args.get('category_id')
    all_category_data = {
        '1': {
            'id': '1',
            'name': '小論文',
            'steps': [
                {'no': 1, 'phase': '理解', 'content': '小論文とは／目的と特徴'},
                {'no': 2, 'phase': '構成', 'content': '序論・本論・結論の作り方'},
                {'no': 3, 'phase': '思考', 'content': '問題把握／主張の立て方／論理展開'},
                {'no': 4, 'phase': '表現', 'content': '文体／語彙／文法／接続詞'},
                {'no': 5, 'phase': '実践', 'content': '添削／推敲／模擬問題／評価基準の理解'}
            ]
        },
        '2': {
            'id': '2',
            'name': 'ビジネス文書',
            'steps': [
                {'no': 1, 'phase': '理解', 'content': 'ビジネス文書とは／目的と特徴'},
                {'no': 2, 'phase': '構成', 'content': '序論・本論・結論の作り方'},
                {'no': 3, 'phase': '思考', 'content': '問題把握／主張の立て方／論理展開'},
                {'no': 4, 'phase': 'できたら', 'content': 'この辺変更しようね'},
                {'no': 5, 'phase': '', 'content': ''}
            ]
        }
    }
    selected_data = all_category_data.get(category_id, all_category_data['1'])
    return render_template('writing/step_list.html', data=selected_data)

@writing_bp.route('/step_learning')
def step_learning():
  """ステージ一覧ページ"""
  return render_template('writing/step_learning.html')