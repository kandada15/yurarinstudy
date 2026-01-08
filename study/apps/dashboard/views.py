from flask import Blueprint, render_template
from apps.extensions import db 
from sqlalchemy import func

#各モデルのインポート
from apps.task.models import Task, Submission, Streamed
from apps.crud.models import Student, Group, Admin

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    template_folder="templates",
    static_folder="static"
)

@dashboard_bp.route('/')
def index():
    # --- 1. プロフィール情報 (仮でID=1の管理者を表示する場合) ---
    # 実際は current_user などを使います
    # admin = Admin.query.filter_by(admin_id='admin01').first() 
    
    # --- 2. グループごとの人数 ---
    # グループ名と、そのグループに所属する生徒数を取得
    # SQLイメージ: SELECT group_name, COUNT(student_id) FROM group JOIN student ...
    # ここでは簡易的に全グループを取得してループ処理する例を書きます
    groups = Group.query.all()
    group_data = []
    for g in groups:
        count = Student.query.filter_by(group_id=g.group_id).count()
        group_data.append({"name": g.group_name, "count": count})

    # --- 3. 課題管理の集計 ---
    # 累計課題配信件数 (Streamedテーブルの全件数)
    streamed_count = Streamed.query.count()

    # 未添削課題件数 (提出済み(submit_flag=True) かつ 未添削(checked_flag=False))
    unchecked_count = Submission.query.filter_by(submit_flag=True, check_flag=False).count()

    # 提出済み件数
    submitted_count = Submission.query.filter_by(submit_flag=True).count()

    # 未提出課題件数 (submit_flag=False)
    unsubmitted_count = Submission.query.filter_by(submit_flag=False).count()

    # --- 4. 学習進捗 (全体の提出率など) ---
    # 例: 全提出物の中で「提出済み」が何％あるか
    total_submissions = Submission.query.count()
    if total_submissions > 0:
        progress_rate = round((submitted_count / total_submissions) * 100)
    else:
        progress_rate = 0

    # 画面(HTML)にデータを渡す
    return render_template(
        'dashboard/dashboard.html',
        group_data=group_data,
        streamed_count=streamed_count,
        unchecked_count=unchecked_count,
        submitted_count=submitted_count,
        unsubmitted_count=unsubmitted_count,
        progress_rate=progress_rate
    )