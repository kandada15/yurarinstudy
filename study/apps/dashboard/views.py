import json
import os
from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request
from apps.task.dao.streamed_dao import StreamedDao
from apps.task.dao.submission_dao import SubmissionDao2
from apps.dashboard.dao.dashboard_dao import DashboardDao

dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates', static_folder='static')

# 生徒ID（s...）を弾く
@dashboard_bp.before_request
def restrict_access():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    if user_id.startswith('s'):
        return redirect(url_for('writing.index'))

@dashboard_bp.route('/')
def index():
    admin_id = session.get('user_id')
    
    # 各DAOの初期化
    d_dao = DashboardDao() 
    s_dao = StreamedDao()
    sub_dao = SubmissionDao2()
    
    # 統計情報の取得
    streamed_count = s_dao.get_streamed_count(admin_id)
    weekly_deadline = s_dao.get_weekly_deadline_count()
    sub_stats = sub_dao.get_stats()
    unsubmitted_count = max(0, streamed_count - sub_stats["submitted_count"])
    real_groups = d_dao.find_groups_for_progress(admin_id)

    return render_template(
        'dashboard/dashboard.html',
        admin={
            "admin_id": admin_id, 
            "admin_name": session.get('user_name', '管理者')
        },
        groups=real_groups, 
        streamed_count=streamed_count,
        unchecked_count=sub_stats["unchecked_count"],
        submitted_count=sub_stats["submitted_count"],
        unsubmitted_count=unsubmitted_count,
        weekly_deadline_count=weekly_deadline
    )

# --- dashboard_bp の中にまとめる ---

# 1. 学習状況トップ（グループ選択）
@dashboard_bp.route('/progress') 
def progress_top():
    d_dao = DashboardDao()
    admin_id = session.get('user_id')
    groups = d_dao.find_groups_for_progress(admin_id)
    return render_template('dashboard/leaning_pro_top.html', groups=groups)

# 2. 生徒一覧
@dashboard_bp.route('/progress/group/<group_id>', methods=['GET']) 
def student_list(group_id):
    d_dao = DashboardDao()
    admin_id = session.get('user_id')
    #生徒一覧を取得
    students = d_dao.find_students_by_group(group_id)
    all_groups = d_dao.find_groups_for_progress(admin_id)
    #リストの中から、group_id と一致する名前をで探す
    group_name = "不明なグループ"
    for g in all_groups:
        # DBのID(数値)とURLのID(文字列)を比較するため、念のため両方 str() にして合わせる
        if str(g['group_id']) == str(group_id):
            group_name = g['group_name']
            break
    return render_template(
        'dashboard/leaning_pro_stu_list.html', 
        students=students, 
        group_name=group_name
    )

# 3. 個別進捗詳細
@dashboard_bp.route('/progress/student/<student_id>') 
def student_detail(student_id):
    d_dao = DashboardDao()
    # current_dir定義
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.abspath(os.path.join(
        current_dir, '..', 'writing', 'static', 'json', 'steps_data.json'
    ))
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            master_data = json.load(f)
    except FileNotFoundError:
        return f"JSONファイルが見つかりません: {json_path}", 404
    # 進捗を取得
    progress_details = d_dao.get_student_detail_list(student_id)
    # 完了しているフェーズ名をセットにする
    completed_keys = {d['phase_name'] for d in progress_details if d['stage_flag'] == 1}
    #統計の計算
    total_stages = len(master_data)
    completed_stages = len(completed_keys)
    percent = int((completed_stages / total_stages) * 100) if total_stages > 0 else 0

    return render_template(
        'dashboard/leaning_pro.html',
        student_id=student_id,
        master_data=master_data, 
        completed_keys=completed_keys, 
        percent=percent,
        stats={
            'total_count': total_stages, 
            'completed_count': completed_stages
        }
    )

@dashboard_bp.route('/manage')
def group_list():
    admin_id = session.get('user_id')
    d_dao = DashboardDao()
    
    # 1. HTMLのカード表示用に「自分が作ったグループ」を取得
    groups = d_dao.find_groups_for_progress(admin_id)
    
    return render_template('dashboard/group_list.html', groups=groups)

@dashboard_bp.route('/api/students')
def get_students_api():
    """JSの検索機能（モーダル）で使うための全受講者データ"""
    d_dao = DashboardDao()
    students = d_dao.find_all_students()
    # mysql-connectorの辞書形式をそのままJSONとして返す
    return jsonify(students)

@dashboard_bp.route('/api/group/<group_id>/members')
def get_group_members(group_id):
    """特定のグループに所属する受講生の一覧を返すAPI"""
    d_dao = DashboardDao()
    # DAOの find_students_by_group を使用
    members = d_dao.find_students_by_group(group_id)
    return jsonify(members)

@dashboard_bp.route('/api/group/add-members', methods=['POST'])
def add_group_members():
    data = request.json
    print(f"--- 届いたデータ: {data} ---") # これをターミナルで確認！

    group_id = data.get('group_id')
    student_ids = data.get('student_ids')
    
    # 400エラーを出している犯人はここ
    if not group_id or not student_ids:
        return jsonify({"success": False, "message": "データ不足"}), 400

    d_dao = DashboardDao()
    success = d_dao.update_students_group(group_id, student_ids)

    if success:
        return jsonify({"success": True, "message": "メンバーを追加しました"})
    else:
        return jsonify({"success": False, "message": "DB更新に失敗しました"}), 500
    
@dashboard_bp.route('/api/group/remove-member', methods=['POST'])
def remove_group_member():
    data = request.json
    student_id = data.get('student_id')

    if not student_id:
        return jsonify({"success": False, "message": "受講生IDが指定されていません"}), 400

    d_dao = DashboardDao()
    success = d_dao.remove_student_from_group(student_id)

    if success:
        return jsonify({"success": True, "message": "メンバーを削除しました"})
    else:
        return jsonify({"success": False, "message": "削除処理に失敗しました"}), 500
    
@dashboard_bp.route('/api/group/update', methods=['POST'])
def update_group():
    data = request.json
    group_id = data.get('group_id')
    group_name = data.get('group_name')

    if not group_id or not group_name:
        return jsonify({"success": False, "message": "入力が正しくありません"}), 400

    d_dao = DashboardDao()
    success = d_dao.update_group_name(group_id, group_name)

    if success:
        return jsonify({"success": True, "message": "グループ名を更新しました"})
    else:
        return jsonify({"success": False, "message": "データベースの更新に失敗しました"}), 500

@dashboard_bp.route('/group/create', methods=['GET', 'POST'])
def group_create():
    d_dao = DashboardDao()
    if request.method == 'POST':
        data = request.json
        group_name = data.get('group_name')
        admin_id = session.get('user_id') 
        # DAOに「グループ名」と「管理者のID」を渡す
        success, message = d_dao.create_group(group_name, admin_id)
        return jsonify({"success": success, "message": message})
    return render_template('dashboard/group_create.html')