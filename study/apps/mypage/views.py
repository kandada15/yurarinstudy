from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
import os
import json
from apps.mypage.dao.mypage_dao import MypageDao

mypage_bp = Blueprint('mypage', __name__, template_folder='templates', static_folder='static')
m_dao = MypageDao()

# 管理者ID（a...）を弾く
@mypage_bp.before_request
def restrict_access():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    if user_id.startswith('a'):
        return redirect(url_for('dashboard.index'))

@mypage_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session.get('user_id')
    profile = m_dao.get_user_profile(user_id)
    group_info = m_dao.get_user_group(user_id)
    tasks = m_dao.get_task_summary(user_id)
    progress_stats = m_dao.get_student_stats(user_id)

    # 進捗率と円グラフの計算 (外周 251.2)
    comp = progress_stats['completed_count'] or 0
    total = progress_stats['total_count'] or 1
    
    percent = int((comp / total) * 100)
    stroke_offset = 251.2 * (1 - percent / 100)

    return render_template(
        'mypage/mypage.html', 
        user=profile, 
        tasks=tasks, 
        group=group_info,
        percent=percent, 
        offset=stroke_offset,
        comp=comp,
        total=total
    )

@mypage_bp.route('/pass_reset')
def pass_reset():
    # パスワード再設定画面を表示
    return render_template('mypage/pass_reset.html')

@mypage_bp.route('/detail/<student_id>')
def detail(student_id):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.abspath(os.path.join(
        current_dir, '..', 'writing', 'static', 'json', 'steps_data.json'
    ))

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            master_data = json.load(f)
    except FileNotFoundError:
        return f"JSONファイルが見つかりません: {json_path}", 404
    progress_details = m_dao.get_student_detail_list(student_id)
    
    completed_keys = {d['phase_name'] for d in progress_details if d['stage_flag'] == 1}

    # 統計の計算
    total_stages = len(master_data)
    completed_stages = len(completed_keys)
    percent = int((completed_stages / total_stages) * 100) if total_stages > 0 else 0
    return render_template(
        'mypage/learning_pro_dis.html',
        student_id=student_id,
        master_data=master_data, 
        completed_keys=completed_keys, 
        percent=percent,
        stats={
            'total_count': total_stages, 
            'completed_count': completed_stages
        }
    )

@mypage_bp.route("/repassword", methods=["GET", "POST"])
def repassword():
    student_id = session.get("user_id")
    
    if request.method == "POST":
        data = request.get_json()
        new_password = data.get("password")

        # 3. 準備したインスタンスを使って、パスワード再設定メソッドを呼ぶ
        # メソッド名が update_password だと仮定しています
        success = m_dao.update_password(student_id, new_password)

        if success:
            return jsonify({"status": "success", "message": "パスワードを更新しました。"})
        else:
            return jsonify({"status": "error", "message": "更新に失敗しました。"}), 500
    return render_template("mypage/repassword.html")