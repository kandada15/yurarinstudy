import json
import os
from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify, current_app
from apps.writing.dao.writing_dao import WritingDao

writing_bp = Blueprint('writing', __name__, template_folder='templates', static_folder='static')
w_dao = WritingDao()

def load_learning_data():
    """別ファイルのJSONを読み込む補助関数"""
    json_path = os.path.join(current_app.root_path, 'writing', 'static', 'json', 'steps_data.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

# --- 1. トップ画面 ---
@writing_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    data = {'page_title': 'ライティング学習', 'select_message': 'コンテンツを選択してください。'}
    return render_template('writing/writing_top.html', data=data)

# --- 2. ステップ一覧画面 (TypeError 対策済み) ---
@writing_bp.route('/step_list/<int:category_id>')
def step_list(category_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    student_id = session.get('user_id')
    progress_data = w_dao.get_user_progress(student_id, category_id)
    completed_list = [row['phase_name'] for row in progress_data if row['stage_flag']]
    
    data = {'name': w_dao.get_category_name(category_id), 'category_id': category_id}
    
    # JSONファイルを読み込んで渡すことで TypeError を回避します
    learning_data = load_learning_data()
    
    return render_template('writing/step_list.html', 
                            data=data, 
                            category_id=category_id, 
                            completed_list=completed_list,
                            learning_data=learning_data)

# --- 3. 学習画面 (UndefinedError 対策済み) ---
@writing_bp.route('/step_learning')
def learning_page():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    phase_name = request.args.get('stage_no')
    category_id = request.args.get('category_id', '1')

    # テンプレート内の {{ data.page_title }} 等に対応
    data = {
        'name': phase_name,
        'page_title': '学習中',
        'category_id': category_id
    }
    
    return render_template('writing/step_learning.html', data=data)

# --- 4. 進捗更新処理 ---
@writing_bp.route('/update_progress', methods=['POST'])
def update_progress():
    if 'user_id' not in session: return jsonify({'status': 'error'}), 401
    req_data = request.get_json()
    phase_name = req_data.get('stage_no')
    w_dao.update_stage_progress(session.get('user_id'), phase_name)
    return jsonify({'status': 'success'})