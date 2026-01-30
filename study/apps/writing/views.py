import json
import os
from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for,
    jsonify,
    current_app,
)
from apps.writing.dao.dao_writing import WritingDao

# Blueprintの作成
writing_bp = Blueprint(
    "writing",
    __name__,
    # 使用するテンプレートフォルダ
    template_folder="templates",
    # 専用の静的ファイル(CSS,JS,画像など)を置くフォルダ
    static_folder="static",
)

# DAO作成
w_dao = WritingDao()

# JSON読み込み(ステップ一覧の内容を外部JSONで管理)
def load_learning_data():
    json_path = os.path.join(
        current_app.root_path, 
        "writing", 
        "static", 
        "json", 
        "steps_data.json"
    )
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    # 読み込み失敗時
    except Exception:
        return {}

# トップページ
@writing_bp.route("/")
def index():
    # ログインしていない場合ログイン画面へリダイレクト
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    # テンプレートに渡すデータを作成
    data = {
        "page_title": "ライティング学習",
        "select_message": "コンテンツを選択してください。",
    }
    # ライティング学習トップページを表示
    return render_template("writing/writing_top.html", data=data)

# カテゴリ別ステップ一覧画面
@writing_bp.route("/step_list/<int:category_id>")
def step_list(category_id):
    # ログインしていない場合ログイン画面へリダイレクト
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    # ログイン中の受講者ID,進捗状況を取得
    student_id = session.get("user_id")
    progress_data = w_dao.get_user_progress(student_id, category_id)
    # 学習済ステップだけをリストにまとめる
    completed_list = [row["phase_name"] for row in progress_data if row["stage_flag"]]

    # テンプレートに渡すデータを作成
    data = {
        "name": w_dao.get_category_name(category_id), 
        "category_id": category_id
    }

    # JSONのステップ一覧データ読み込み
    learning_data = load_learning_data()

    # ステップ一覧画面表示
    return render_template(
        "writing/step_list.html",
        data=data,
        category_id=category_id,
        completed_list=completed_list,
        learning_data=learning_data,
    )

# 学習画面
@writing_bp.route("/step_learning")
def learning_page():
    # ログインしていない場合ログイン画面へリダイレクト
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    # ステップ名,カテゴリIDを取得
    phase_name = request.args.get("stage_no")
    category_id = request.args.get("category_id", "1")

    # テンプレートに渡すデータを作成
    data = {
        "name": phase_name,
        "page_title": "学習中", 
        "category_id": category_id
    }

    # 学習画面を表示
    return render_template("writing/step_learning.html", data=data)

# 進捗更新
@writing_bp.route("/update_progress", methods=["POST"])
def update_progress():
    # ログインしていない場合エラーを返す
    if "user_id" not in session:
        return jsonify({"status": "error"}), 401
    
    req_data = request.get_json()
    phase_name = req_data.get("stage_no")
    
    # DAOを使用しDBの進捗を更新
    w_dao.update_stage_progress(session.get("user_id"), phase_name)
    
    # 成功レスポンスを返す
    return jsonify({"status": "success"})