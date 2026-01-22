from flask import Blueprint, render_template, request, session
from apps.app import db
from apps.writing.models import Progress

# Blueprintの作成
writing_bp = Blueprint(
    "writing",
    __name__,
    # 使用するテンプレートフォルダ
    template_folder="templates",
    # 専用の静的ファイル(CSS,JS,画像など)を置くフォルダ
    static_folder="static",
)

# ルーティングの定義
@writing_bp.route("/")
def index():
    """ライティングトップ / カテゴリ一覧ページ"""
    static_categories = [
        {"task_id": 1, "task_name": "小論文"},
        {"task_id": 2, "task_name": "ビジネス文書"},
        {"task_id": 3, "task_name": "レポート"},
        {"task_id": 4, "task_name": "表現トレーニング"},
    ]
    data = {
        "page_title": "ライティング課題",
        "select_message": "学習したいコンテンツを選択してください",
        "categories": static_categories,
    }

    return render_template("writing/writing_top.html", data=data)


@writing_bp.route("/step_list")
def step_list():
    category_id = request.args.get("category_id")
    student_id = session.get("user_id")
    category_names = {
        "1": "小論文",
        "2": "ビジネス文書",
        "3": "レポート",
        "4": "表現トレーニング",
    }
    data = {
        "name": category_names.get(category_id, "不明なカテゴリー"),
        "id": category_id,
    }

    completed_stages = (
        db.session.query(Progress.phase_name)
        .filter_by(student_id=student_id, stage_flag=True)
        .all()
    )

    completed_list = [p.phase_name for p in completed_stages]

    return render_template(
        "writing/step_list.html",
        data=data,
        category_id=category_id,
        completed_list=completed_list,
    )


@writing_bp.route("/step_learning")
def step_learning():
    """ステップ学習ページ"""
    category_id = request.args.get("category_id")
    stage_no = request.args.get("stage_no")

    # 2. テンプレートにそれらの値を渡す
    return render_template(
        "writing/step_learning.html", category_id=category_id, stage_no=stage_no
    )


@writing_bp.route("/update_progress", methods=["POST"])
def update_progress():
    data = request.get_json()
    category_id = data.get("category_id")
    stage_no = data.get("stage_no")

    # ログイン中のユーザーIDをセッションから取得（例）
    student_id = session.get("user_id")

    if not student_id:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    # --- DB更新ロジック ---
    # progressテーブルの stage_flag を 1 (True) に更新する
    # ※phase_name を stage_no から特定するか、stage_no 自体を管理に使う

    try:
        # SQL実行例:
        # UPDATE progress SET stage_flag = 1
        # WHERE student_id = %s AND phase_name = %s

        # ※ もしレコードがなければ INSERT、あれば UPDATE する処理が必要
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500