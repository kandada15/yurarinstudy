from flask import Blueprint, render_template, request, session, jsonify
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
    # DBの student_id カラムに合わせて文字列に変換
    student_id = str(session.get('user_id', '')) 

    # DBから完了済みのレコードを取得（stage_flagはBoolean）
    completed_records = Progress.query.filter_by(
        student_id=student_id,
        stage_flag=True
    ).all()
    
    # 完了済みの phase_name リストを作成
    completed_list = [r.phase_name for r in completed_records]

    category_names = {'essay': '小論文', 'business': 'ビジネス文書'}
    data = {'name': category_names.get(category_id, 'ライティング')}

    return render_template('writing/step_list.html', 
                            category_id=category_id, 
                            data=data,
                            completed_list=completed_list)

@writing_bp.route('/step_learning')
def step_learning():
    """学習画面"""
    category_id = request.args.get('category_id')
    stage_no = request.args.get('stage_no')
    return render_template('writing/step_learning.html', 
                            category_id=category_id, 
                            stage_no=stage_no)

@writing_bp.route('/update_progress', methods=['POST'])
def update_progress():
    """進捗更新"""
    data = request.get_json(force=True, silent=True)
    stage_val = data.get('stage_no')
    student_id = str(session.get('user_id', ''))

    if not student_id or not stage_val:
        return jsonify({'status': 'error', 'message': 'データ不足'}), 400

    try:
        # DBのカラム名 phase_name で検索
        progress = Progress.query.filter_by(
            student_id=student_id, 
            phase_name=stage_val
        ).first()

        if progress:
            progress.stage_flag = True # 完了(True)に更新
        else:
            new_progress = Progress(
                student_id=student_id,
                phase_name=stage_val, # DBのカラム名に合わせる
                stage_flag=True
            )
            db.session.add(new_progress)
        
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500