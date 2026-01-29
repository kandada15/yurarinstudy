from flask import Blueprint, render_template, redirect, url_for, current_app,  json, jsonify, request,  session

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

# DAO-インスタンス化
student_dao = StudentDao()
admin_dao = AdminDao()

# ルーティングの定義
@crud_bp.route("/manage")
def user_manage():
    admin_id = session.get('user_id')
    if not admin_id:
        return redirect(url_for('auth.login'))
    
    all_students = student_dao.find_all_groupname()
    all_admins = admin_dao.find_all_groupname()

    return render_template(
        "crud/user_info_list.html",
        all_students=all_students,
        all_admins=all_admins
    )

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
    # クエリパラメータ ?query=xxx を取得
    # search_query = request.args.get('query', '')
    # user_type = request.args.get("type")
    
    # # DAOを使用してMySQLから検索
    # # SQLイメージ: SELECT * FROM users WHERE id LIKE %q% OR name LIKE %q% OR groups LIKE %q%

    # if user_type == "student":
    #     if search_query:
    #         results = student_dao.search_students(search_query)
    #     else:
    #         results = student_dao.find_all_groupname()

    #     user_list = [{
    #         "id": s.student_id,
    #         "name": s.student_name,
    #         "group_name": s.group_name
    #     } for s in results]

    # elif user_type == "admin":
    #     if search_query:
    #         results = admin_dao.search_admins(search_query)
    #     else:
    #         results = admin_dao.find_all_groupname()

    #     user_list = [{
    #         "id": a.admin_id,
    #         "name": a.admin_name,
    #         "group_name": a.group_name
    #     } for a in results]

    # else:
    #     return jsonify({
    #         "status": "error",
    #         "message": "invalid type"
    #     }), 400

    # return jsonify({
    #     "status": "success",
    #     "type": user_type,
    #     "users": user_list
    # })

