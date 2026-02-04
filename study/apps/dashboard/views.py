import json
import os
from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request
from apps.task.dao.streamed_dao import StreamedDao
from apps.task.dao.submission_dao import SubmissionDao, SubmissionDao2
from apps.crud.dao.group_dao import GroupDao  # 修正したDaoをインポート
from apps.dashboard.dao.dao_dashboard import Dashboard_DAO
from apps.dashboard.dao.dashboard_dao import DashboardDao

dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates', static_folder='static')

# 各DAOの初期化
# ルート外に置く
s_dao = StreamedDao()
sub_dao = SubmissionDao2()
g_dao = GroupDao()  # 新しく作成
d_dao = DashboardDao()
D_dao = Dashboard_DAO()

# 生徒ID（s...）を弾く
@dashboard_bp.before_request
def restrict_access():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    if user_id.startswith('s'):
        return redirect(url_for('mypage.index'))

@dashboard_bp.route('/')
def index():
    admin_id = session.get('user_id')
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


# 1. 学習状況トップ（グループ選択）
@dashboard_bp.route('/progress') 
def progress_top():
    admin_id = session.get('user_id')
    groups = d_dao.find_groups_for_progress(admin_id)
    return render_template('dashboard/leaning_pro_top.html', groups=groups)

# 2. 生徒一覧
@dashboard_bp.route('/progress/group/<group_id>', methods=['GET']) 
def student_list(group_id):
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
    
    # 1. HTMLのカード表示用に「自分が作ったグループ」を取得
    groups = d_dao.find_groups_for_progress(admin_id)
    
    return render_template('dashboard/group_list.html', groups=groups)

@dashboard_bp.route('/api/students')
def get_students_api():
    """JSの検索機能（モーダル）で使うための全受講者データ"""
    students = d_dao.find_all_students()
    # mysql-connectorの辞書形式をそのままJSONとして返す
    return jsonify(students)

@dashboard_bp.route('/api/group/<group_id>/members')
def get_group_members(group_id):
    """特定のグループに所属する受講生の一覧を返すAPI"""
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

    success = d_dao.update_group_name(group_id, group_name)

    if success:
        return jsonify({"success": True, "message": "グループ名を更新しました"})
    else:
        return jsonify({"success": False, "message": "データベースの更新に失敗しました"}), 500

@dashboard_bp.route('/group/create', methods=['GET', 'POST'])
def group_create():
    if request.method == 'POST':
        data = request.json
        group_name = data.get('group_name')
        admin_id = session.get('user_id') 
        # DAOに「グループ名」と「管理者のID」を渡す
        success, message = d_dao.create_group(group_name, admin_id)
        return jsonify({"success": success, "message": message})
    return render_template('dashboard/group_create.html')

"""  
以下より、ダッシュボード/課題返却機能
"""

""" 配信済み課題一覧の表示 """
@dashboard_bp.route("/streamed")
def streamed_list():
    admin_id = session.get('user_id')
    all_tasks = s_dao.find_streamed_for_student(admin_id)

    # ページネーションの設定
    page = request.args.get('page', 1, type=int)
    per_page = 4 # 1ページあたりの表示件数
    offset = (page - 1) * per_page

    # DAOにoffsetとlimitを渡して取得するように変更
    # 簡易的なページネーション処理
    tasks = all_tasks[offset : offset + per_page]

    # 次のページがあるかどうかの判定
    has_next = len(all_tasks) > offset + per_page
    has_prev = page > 1

    return render_template("dashboard/deli_task_list.html", tasks=tasks, has_next=has_next, has_prev=has_prev)

""" 課題を配信された学生の一覧表示 """
@dashboard_bp.route("/streamed/student/<int:streamed_id>")
def streamed_student_list(streamed_id):
    admin_id = session.get('user_id')
    streamed = D_dao.find_streamed_name_by_id(streamed_id)
    keyword = request.args.get("keyword")
    # 配信済みかつ提出/添削のフラグが関連しているdaoを作成
    streamed_student = D_dao.find_students_status_by_streamed_id(streamed_id, admin_id, keyword)
    return render_template("dashboard/task_stu_list.html", streamed_name=streamed["streamed_name"], streamed_student=streamed_student, streamed_id=streamed_id)

""" 受講者(課題提出済み)の添削画面を表示 """
@dashboard_bp.route("/streamed/student/<int:submission_id>/correction", methods=["GET"])
def task_correction(submission_id):
    admin_id = session.get('user_id')
    # 添削画面にて必要な成功をdaoにて取得する。
    correction_student = D_dao.find_submission_by_streamed_id(submission_id, admin_id)
    return render_template("dashboard/correct_write.html", correction_student=correction_student, submission_id=submission_id, streamed_id=correction_student["streamed_id"])

""" 添削完了後、確認画面→DB登録まで """
@dashboard_bp.route("/streamed/student/<int:submission_id>/correction", methods=["POST"])
def submit_correction(submission_id):
    # 添削した解答文を取得する
    corrected_answer = request.form.get("answer_text")
    streamed_id = request.form.get("streamed_id")

    D_dao.update_submission_correction(submission_id, corrected_answer)
    return ("", 204)


""" 
以下、ダッシュボードの添削済み課題を提出するためのコード(仮-動きません)
html,css,js待ち
"""

""" 配信済みかつ未添削課題を探す。あれば、error-messageを返す """
@dashboard_bp.route("/streamed/student/return/check", methods=["POST"])
def check_can_return():
    streamed_id = request.form.get("streamed_id")
    has_unchecked =  D_dao.exists_unchecked_submission(streamed_id)

    if has_unchecked:
        return jsonify({
            "can_return": False,
            "status": "error",
            "message": "未添削の課題があります"
        })
    
    return jsonify({
        "can_return": True
    })

""" 返却フラグを更新して、値を返す """
@dashboard_bp.route("/streamed/student/return", methods=["POST"])
def correction_return():
    streamed_id = request.form.get("streamed_id")

    # バリデーション(配信IDの有無)
    if not streamed_id:
      return jsonify({
        "status": "error",
        "message": "streamed_id が取得できません"
      }), 400
    
    update_flag = D_dao.exists_flag_check(streamed_id)
    if update_flag:
        return jsonify({
            "stasus": "error",
            "message": "未提出または未添削の課題があります"
        }), 400
    
    # 全員、「添削済み」のときのみ動かす
    D_dao.update_return_flag(streamed_id)

    return jsonify({
        "status": "success",
        "message": "課題の返却が完了しました"
    })


""" 返却済み課題の表示 """
@dashboard_bp.route("returned/groups")
def returned_group_list():
    return render_template("dashboard/returned_task/past_task_view.html")
   
