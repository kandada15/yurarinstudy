from flask import Blueprint, render_template, session

from apps.crud.dao.student_dao import StudentDao

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

# ルーティングの定義
@crud_bp.route("/manage")
def user_manage():
    student_id = session.get('user_id')
    # all_students = student_dao.find_all(student_id)
    return render_template("crud/user_info_list.html")
