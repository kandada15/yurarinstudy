from flask import Blueprint, render_template, session, redirect, url_for
from study.apps.task.dao.dao_streamed import StreamedDao
from study.apps.task.dao.dao_submission import SubmissionDao2
from study.apps.crud.dao.dao_group import GroupDao  # 修正したDaoをインポート

dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates', static_folder='static')

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
    
    # 各DAOの初期化
    s_dao = StreamedDao()
    sub_dao = SubmissionDao2()
    g_dao = GroupDao()  # 新しく作成
    
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