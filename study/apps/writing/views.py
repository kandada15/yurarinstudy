from flask import Blueprint, redirect, render_template, abort
from apps.app import db 
from apps.writing.models import Category 

# アプリの作成 (省略なし)
writing = Blueprint(
  'writing',
  __name__,
  template_folder='templates',
  static_folder='static'
)

# ライティングトップページ
@writing.route('/writing')
def writing_top():
    # サンプルデータ
    sample_categories = [
        {'category_id': '1', 'category_name': '小論文'},
        {'category_id': '2', 'category_name': 'ビジネス文書'},
        {'category_id': '3', 'category_name': 'レポート'},
        {'category_id': '4', 'category_name': '表現トレーニング'},
    ]
    
    context_data = {
        'page_title': 'ライティング学習',
        'select_message': '学習したいコンテンツを選択してください:',
        # テンプレートが期待するキー名 ('categories') でリストを渡す
        'categories': sample_categories 
    }
    return render_template('writing/writing_top.html', data=context_data)
@writing.route('/category/<string:category_id>')
def category_detail(category_id):
    # トップページと同じサンプルデータを使用
    sample_categories = [
        {'category_id': '1', 'category_name': '小論文'},
        {'category_id': '2', 'category_name': 'ビジネス文書'},
        {'category_id': '3', 'category_name': 'レポート'},
        {'category_id': '4', 'category_name': '表現トレーニング'},
    ]
    
    # 渡されたIDに一致するカテゴリ名を探す
    selected_category = next((c for c in sample_categories if c['category_id'] == category_id), None)
    
    if selected_category:
        context_data = {
            # カテゴリ名だけを渡す
            'page_title': selected_category['category_name'] 
        }
        # テンプレートは 'writing/category_detail.html' である必要があります
        return render_template('writing/category_detail.html', data=context_data)
    else:
        # IDが見つからなければ404を返す
        abort(404)