from flask import Blueprint, render_template, redirect, url_for, current_app,  jsonify, request,  session
from apps.crud.dao.dao_student import StudentDao
from apps.crud.dao.dao_admin import AdminDao

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

# ユーザ詳細画面
@crud_bp.route("/detail")
def user_detail():
    user_data = {
        "id": "S000123",
        "name": "山田 太郎",
        "role": "student"
    }
    return render_template("crud/user_info_inq.html", user_data=user_data)

@crud_bp.route("/user_add")
def user_add():
    return render_template("crud/new_user_add.html")

@crud_bp.route("/user/reset_password", methods=['POST'])
def reset_password():
    data = request.get_json(silent=True)
    user_id = data.get('user_id')

    return jsonify({"status": "success", "message": f"User {user_id} password reset."})

@crud_bp.route("/user/delete", methods=['POST'])
def delete_user():
    data = request.get_json(silent="True")
    user_id = data.get('user_id')

    return jsonify({"status": "success", "message": f"User {user_id} deleted."})

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
    user_type = data.get("type")

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
    user_type = data.get("type")

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