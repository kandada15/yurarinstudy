from flask import Blueprint, render_template, redirect, url_for, current_app,  jsonify, request,  session
from apps.crud.dao.dao_student import StudentDao
from apps.crud.dao.dao_admin import AdminDao
from apps.dashboard.dao.dashboard_dao import DashboardDao
import os
import json

# Blueprintの作成
crud_bp = Blueprint(
    "crud",
    __name__,
    # 使用するテンプレートフォルダ
    template_folder="templates",
    # 専用の静的ファイル(CSS,JS,画像など)を置くフォルダ
    static_folder="static",
)

# DAO作成
student_dao = StudentDao()
admin_dao = AdminDao()
d_dao = DashboardDao()

# ルーティングの定義
# ユーザ一覧画面
@crud_bp.route("/manage")
def user_manage():
    admin_id = session.get('user_id')
    # ログインしていない場合ログイン画面へリダイレクト
    if not admin_id:
        return redirect(url_for('auth.login'))
    
    # 管理者,受講者一覧取得
    all_students = student_dao.find_all_groupname()
    all_admins = admin_dao.find_all_groupname()

    # ユーザ一覧画面表示
    return render_template(
        "crud/user_info_list.html",
        all_students=all_students,
        all_admins=all_admins
    )

@crud_bp.route("/user_add")
def user_add():
    return render_template("crud/new_user_add.html")

@crud_bp.route("/api/user/search", methods=['GET'])
def search_users():
    try:
        search_query = request.args.get('query', '')
        user_type = request.args.get("type")

        if user_type == "student":
            if search_query:
                results = student_dao.search_students(search_query)
            else:
                results = student_dao.find_all_groupname()

            user_list = [{
                "id": s.student_id,
                "name": s.student_name,
                "group_name": s.group_name
            } for s in results]

        elif user_type == "admin":
            if search_query:
                results = admin_dao.search_admins(search_query)
            else:
                results = admin_dao.find_all_groupname()

            user_list = [{
                "id": a.admin_id,
                "name": a.admin_name,
                "group_name": a.group_name
            } for a in results]

        else:
            return jsonify({
                "status": "error",
                "message": "invalid type"
            }), 400

        return jsonify({
            "status": "success",
            "type": user_type,
            "users": user_list
        })

    except Exception as e:
        current_app.logger.exception(e)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# ============================================
# パスワードリセット API
# ============================================
@crud_bp.route("/api/user/reset_password", methods=["POST"])
def api_reset_password():
    data = request.json
    # ターミナルで中身を確認するためのデバッグ
    print(f"--- パスワードリセットリクエスト ---")
    print(f"受信データ: {data}")

    if not data:
        return jsonify({"status": "error", "message": "データが空です"}), 400

    user_id = data.get("user_id")
    user_type = data.get("user_type")

    success = False
    try:
        if user_type == "admin":
            # AdminDao の reset_password を実行
            success = admin_dao.reset_password(user_id)
        else:
            # StudentDao の reset_password を実行
            success = student_dao.reset_password(user_id)
        
        if success:
            return jsonify({"status": "success", "message": "パスワードをリセットしました"})
        else:
            return jsonify({"status": "error", "message": "対象のユーザが見つかりませんでした"}), 400

    except Exception as e:
        print(f"エラー発生: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# ============================================
# ユーザ削除 API
# ============================================
@crud_bp.route("/api/user/delete", methods=["POST"])
def api_delete_user():
    data = request.json
    print(f"--- ユーザ削除リクエスト ---")
    print(f"受信データ: {data}")

    if not data:
        return jsonify({"status": "error", "message": "データが空です"}), 400

    user_id = data.get("user_id")
    user_type = data.get("user_type")

    success = False
    try:
        if user_type == "admin":
            success = admin_dao.delete_admin(user_id)
        else:
            success = student_dao.delete_student(user_id)

        if success:
            return jsonify({"status": "success", "message": "ユーザを削除しました"})
        else:
            return jsonify({"status": "error", "message": "削除に失敗しました"}), 400

    except Exception as e:
        print(f"エラー発生: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
@crud_bp.route("/new_user_add", methods=["GET", "POST"])
def new_user_add():
    if request.method == "POST":
        data = request.get_json()
        print(f"DEBUG: 受信データ = {data}")
        
        user_type = data.get("user_type")  # 'admin' or 'student'
        u_id      = data.get("user_id")
        name      = data.get("user_name")
        password  = data.get("password")  # JS側で生成した8桁数値
        birthday  = data.get("birthday")
        # 登録処理
        success = admin_dao.register_user(u_id, name, password, birthday, user_type)

        if success:
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error", "message": "登録に失敗しました。"}), 500

    return render_template("crud/new_user_add.html")

@crud_bp.route("/user_info/<user_type>/<user_id>")
def user_info(user_type, user_id):
    user = admin_dao.find_by_id(user_id, user_type)
    
    if not user:
        return "ユーザーが見つかりません", 404
    # 初期値
    percent = 0
    m_data = {}

    # 受講者の場合のみ進捗を計算する
    if user_type == 'student':
        # 1. JSON（マスタデータ）を読み込む
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.abspath(os.path.join(
            current_dir, '..', 'writing', 'static', 'json', 'steps_data.json'
        ))
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                m_data = json.load(f)
        except FileNotFoundError:
            m_data = {}

        # 2. 進捗データをDBから取得して計算
        progress_details = d_dao.get_student_detail_list(user_id)
        # stage_flag が 1 のフェーズ名だけを抜き出す
        completed_keys = {d['phase_name'] for d in progress_details if d['stage_flag'] == 1}
        
        total_stages = len(m_data)
        completed_stages = len(completed_keys)
        
        # 3. ％を計算
        if total_stages > 0:
            percent = int((completed_stages / total_stages) * 100)
    
    return render_template(
        "crud/user_info.html", 
        user=user, 
        user_type=user_type, 
        percent=percent, 
        master_data=m_data
    )

@crud_bp.route("/student_tasks/<student_id>")
def stu_task_list(student_id):
    # 受講生の氏名などを表示するためにプロフィールも取得
    student_profile = student_dao.get_student_by_id(student_id) # 既存のメソッドを想定
    # 返却済み課題リストを取得
    tasks = student_dao.get_student_returned_tasks(student_id)

    return render_template(
        "crud/stu_task_list.html", 
        student=student_profile, 
        tasks=tasks
    )

@crud_bp.route("/student_tasks/<student_id>/detail/<streamed_id>")
def stu_task_detail(student_id, streamed_id):
    # 受講生の詳細データを取得
    task = student_dao.get_student_task_detail(student_id, streamed_id)
    
    if not task:
        return "データが見つかりません", 404

    return render_template("crud/stu_task_detail.html", task=task)

@crud_bp.route("/check_id", methods=["POST"])
def check_id():
    data = request.get_json()
    u_id = data.get("user_id")
    user_type = data.get("user_type") 

    # DAOを使って重複チェック
    exists = admin_dao.check_id_exists(u_id, user_type)
    
    return jsonify({"exists": exists})