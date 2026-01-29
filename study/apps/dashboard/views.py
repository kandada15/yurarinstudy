from flask import Blueprint, render_template, session, redirect, url_for
from apps.task.dao.streamed_dao import StreamedDao
from apps.task.dao.submission_dao import SubmissionDao2
from apps.crud.dao.group_dao import GroupDao
from apps.dashboard.dao.dashboard_dao import DashboardDao

writing_bp = Blueprint('writing', __name__, template_folder='templates', static_folder='static')
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
    d_dao = DashboardDao() 
    s_dao = StreamedDao()
    sub_dao = SubmissionDao2()
    
    # 統計情報の取得
    streamed_count = s_dao.get_streamed_count(admin_id)
    weekly_deadline = s_dao.get_weekly_deadline_count()
    sub_stats = sub_dao.get_stats()
    unsubmitted_count = max(0, streamed_count - sub_stats["submitted_count"])
    real_groups = d_dao.find_groups_for_progress(admin_id)

    return render_template(
        'dashboard/dashboard.html',
        admin={
            "admin_id": admin_id, 
            "admin_name": session.get('user_name', '管理者')
        },
        groups=real_groups, 
        streamed_count=streamed_count,
        unchecked_count=sub_stats["unchecked_count"],
        submitted_count=sub_stats["submitted_count"],
        unsubmitted_count=unsubmitted_count,
        weekly_deadline_count=weekly_deadline
    )

    # writingブループリント内
d_dao = DashboardDao()

# 1. 学習状況トップ（グループ選択）
@writing_bp.route('/progress')
def progress_top():
    admin_id = session.get('user_id')
    # メソッド名を DAO の定義に合わせる
    groups = d_dao.find_groups_for_progress(admin_id)
    return render_template('dashboard/leaning_pro_top.html', groups=groups)

# 2. 生徒一覧
@writing_bp.route('/progress/group/<group_id>')
def student_list(group_id):
    students = d_dao.find_students_by_group(group_id)
    return render_template('dashboard/leaning_pro_stu_list.html', students=students)

# 3. 個別進捗詳細
@writing_bp.route('/progress/student/<student_id>')
def student_detail(student_id):
    # 統計データ取得 (DAO側の名前に合わせる)
    stats = d_dao.get_student_stats(student_id)
    
    # キー名を DAO の戻り値 (total_count, completed_count) に合わせる
    total = stats['total_count'] or 0
    completed = stats['completed_count'] or 0
    percent = int((completed / total) * 100) if total > 0 else 0
    
    # テーブル用データ取得 (DAO側の名前に合わせる)
    details = d_dao.get_student_detail_list(student_id)
    
    return render_template('dashboard/leaning_pro.html', 
                            student_id=student_id,
                            stats=stats, 
                            percent=percent, 
                            details=details)