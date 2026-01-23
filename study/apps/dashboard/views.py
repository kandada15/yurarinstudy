from flask import Blueprint, render_template, session, redirect, url_for
from apps.task.dao.streamed_dao import StreamedDao
from apps.task.dao.submission_dao import SubmissionDao

dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates', static_folder='static')

@dashboard_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    admin_id = session.get('user_id')
    
    s_dao = StreamedDao()
    sub_dao = SubmissionDao()
    
    streamed_count = s_dao.get_streamed_count(admin_id)
    weekly_deadline = s_dao.get_weekly_deadline_count()
    sub_stats = sub_dao.get_stats()

    # 未提出数の簡易計算（配信数 - 提出数）
    unsubmitted_count = max(0, streamed_count - sub_stats["submitted_count"])

    return render_template(
        'dashboard/index.html',
        admin={"admin_id": admin_id, "admin_name": session.get('user_name', '管理者')},
        groups=[], # グループ一覧が必要なら別途 GroupDao を作成
        streamed_count=streamed_count,
        unchecked_count=sub_stats["unchecked_count"],
        submitted_count=sub_stats["submitted_count"],
        unsubmitted_count=unsubmitted_count,
        weekly_deadline_count=weekly_deadline
    )