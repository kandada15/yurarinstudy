from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for
from apps.app import db 
from apps.writing.models import Progress 

# Blueprintの作成
writing_bp = Blueprint(
    'writing',
    __name__,
    # 使用するテンプレートフォルダ
    template_folder='templates',
    # 専用の静的ファイル(CSS,JS,画像など)を置くフォルダ
    static_folder='static'
)

# ============================================
# ★ ログインチェックの共通処理
# ============================================
@writing_bp.before_request
def before_request():
    # セッションに user_id がない場合は、ログイン画面へ強制的に飛ばす
    if 'user_id' not in session:
        # 'auth.login' の部分は、実際のログイン画面のエンドポイント名に合わせてください
        return redirect(url_for('auth.login'))

# ============================================
# 1. ライティングトップ
# ============================================
=======
# ルーティングの定義
@writing_bp.route('/')
def index():
    """カテゴリ選択画面"""
    static_categories = [
        {'task_id': 'essay', 'task_name': '小論文'},
        {'task_id': 'business', 'task_name': 'ビジネス文書'},
        {'task_id': 'report', 'task_name': 'レポート'},
        {'task_id': 'training', 'task_name': '表現トレーニング'}
    ]
    data = {
        "page_title": "ライティング課題",
        "select_message": "学習したいコンテンツを選択してください",
        "categories": static_categories,
    }
    return render_template('writing/writing_top.html', data=data)

@writing_bp.route('/step_list')
def step_list():
    """ステージ一覧画面"""
    category_id = request.args.get('category_id', 'essay')
    student_id = str(session.get('user_id', '')) 
    # 履修済ステージをDBから取得(stage_flag=1)
    completed_records = Progress.query.filter_by(
        student_id=student_id,
        stage_flag=True
    ).all()

    # 履修済ステージだけのリスト作成
    completed_list = [r.phase_name for r in completed_records]

    # カテゴリ名
    category_names = {'essay': '小論文', 'business': 'ビジネス文書'}
    data = {'name': category_names.get(category_id, 'ライティング')}

    # データを画面に渡す処理
    return render_template(
        'writing/step_list.html', 
        category_id=category_id, 
        data=data,
        completed_list=completed_list
    )

@writing_bp.route('/step_learning')
def step_learning():
    """学習画面"""
    category_id = request.args.get('category_id')
    stage_no = request.args.get('stage_no')
    
    # データを画面に渡す処理
    return render_template(
        'writing/step_learning.html', 
        category_id=category_id, 
        stage_no=stage_no
    )

@writing_bp.route('/update_progress', methods=['POST'])
def update_progress():
    """進捗更新"""
    data = request.get_json(force=True, silent=True)
    stage_val = data.get('stage_no')
    student_id = str(session.get('user_id', ''))

    # 必須データのチェック(student_id,stage_val)
    if not student_id or not stage_val:
        return jsonify({'status': 'error', 'message': 'データ不足'}), 400

    # 進捗データをDBから条件検索
    try:
        progress = Progress.query.filter_by(
            student_id=student_id, 
            phase_name=stage_val
        ).first()

        # 既存レコードがあれば更新、無ければ新規作成
        if progress:
            progress.stage_flag = True
        else:
            new_progress = Progress(
                student_id=student_id,
                phase_name=stage_val,
                stage_flag=True
            )
            db.session.add(new_progress)
        
        # DBに反映
        db.session.commit()
        return jsonify({'status': 'success'})
    
    # 例外処理
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500