from flask import Blueprint, render_template, session, redirect, url_for, request
from apps.task.dao.streamed_dao import StreamedDao
from apps.task.dao.submission_dao import SubmissionDao2
from apps.crud.dao.group_dao import GroupDao  # 修正したDaoをインポート
from apps.dashboard.dao.dao_dashboard import Dashboard_DAO

dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates', static_folder='static')

# 各DAOの初期化
# ルート外に置く
s_dao = StreamedDao()
sub_dao = SubmissionDao2()
g_dao = GroupDao()  # 新しく作成
d_dao = Dashboard_DAO()

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
    
    # 統計情報の取得
    streamed_count = s_dao.get_streamed_count(admin_id)
    weekly_deadline = s_dao.get_weekly_deadline_count()
    sub_stats = sub_dao.get_stats()
    unsubmitted_count = max(0, streamed_count - sub_stats["submitted_count"])

    real_groups = g_dao.find_by_admin_id(admin_id)

    return render_template(
        'dashboard/dashboard.html',
        admin={
            "admin_id": admin_id, 
            "admin_name": session.get('user_name', '管理者')
        },
        groups=real_groups, # DBから取得した本物のリストを渡す
        streamed_count=streamed_count,
        unchecked_count=sub_stats["unchecked_count"],
        submitted_count=sub_stats["submitted_count"],
        unsubmitted_count=unsubmitted_count,
        weekly_deadline_count=weekly_deadline
    )

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

@dashboard_bp.route("/streamed/student/<int:streamed_id>")
def stedent_list(streamed_id):

    admin_id = session.get('user_id')
    streamed = d_dao.find_streamed_name_by_id(streamed_id)
    keyword = request.args.get("keyword")
    # 配信済みかつ提出/添削のフラグが関連しているdaoを作成
    streamed_student = d_dao.find_students_status_by_streamed_id(streamed_id, admin_id, keyword)
    return render_template("dashboard/task_stu_list.html", streamed_name=streamed["streamed_name"], streamed_student=streamed_student)