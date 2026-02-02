from flask import Blueprint, render_template, session, redirect, url_for
from apps.task.dao.streamed_dao import StreamedDao
from apps.task.dao.dao_submission import SubmissionDao2
from apps.crud.dao.dao_group import GroupDao
from apps.dashboard.dao.dao_dashboard import Dashboard_DAO

# Blueprintの作成
dashboard_bp = Blueprint(
    'dashboard', 
    __name__, 
    # 使用するテンプレートフォルダ
    template_folder='templates',
    # 専用の静的ファイル(CSS,JS,画像など)を置くフォルダ
    static_folder='static'
)

writing_bp = Blueprint(
    'writing',
    __name__,
    # 使用するテンプレートフォルダ
    template_folder='templates',
    # 専用の静的ファイル(CSS,JS,画像など)を置くフォルダ
    static_folder='static'
)

# 各DAOの初期化
# ルート外に置く
s_dao = StreamedDao()
sub_dao = SubmissionDao2()
g_dao = GroupDao()
D_dao = Dashboard_DAO()

# アクセス制限(sから始まる受講者IDを弾く)
@dashboard_bp.before_request
def restrict_access():
    user_id = session.get('user_id')
    # ログインしていない場合ログイン画面へリダイレクト
    if not user_id:
        return redirect(url_for('auth.login'))
    if user_id.startswith('s'):
        return redirect(url_for('writing.index'))

# ダッシュボードトップ画面
@dashboard_bp.route('/')
def index():
    admin_id = session.get('user_id')

    # 配信済課題数を取得
    streamed_count = s_dao.get_streamed_count(admin_id)
    # 今週締切の課題数を取得
    weekly_deadline = s_dao.get_weekly_deadline_count()
    # 提出状況,添削状況を取得
    sub_stats = sub_dao.get_stats()
    # 未提出数計算
    unsubmitted_count = max(0, streamed_count - sub_stats["submitted_count"])
    # 所持グループ一覧取得
    real_groups = g_dao.find_by_admin_id(admin_id)

    # ダッシュボードトップ画面表示
    return render_template(
        'dashboard/dashboard.html',
        admin={
            "admin_id": admin_id, 
            "admin_name": session.get('user_name', '管理者')
        },
        # 所持グループのリスト
        groups=real_groups,
        
        # ダッシュボードに表示する統計情報
        streamed_count=streamed_count,
        unchecked_count=sub_stats["unchecked_count"],
        submitted_count=sub_stats["submitted_count"],
        unsubmitted_count=unsubmitted_count,
        weekly_deadline_count=weekly_deadline
    )

# 学習状況トップ画面（グループ選択）
@writing_bp.route('/progress')
def progress_top():
    admin_id = session.get('user_id')
    groups = d_dao.find_groups_for_progress(admin_id)
    return render_template('dashboard/leaning_pro_top.html', groups=groups)

# 受講者一覧画面
@writing_bp.route('/progress/group/<group_id>')
def student_list(group_id):
    students = d_dao.find_students_by_group(group_id)
    return render_template('dashboard/leaning_pro_stu_list.html', students=students)

# 3. 受講者別学習状況
@writing_bp.route('/progress/student/<student_id>')
def student_detail(student_id):
    stats = d_dao.get_student_stats(student_id)
    total = stats['total_count'] or 0
    completed = stats['completed_count'] or 0
    percent = int((completed / total) * 100) if total > 0 else 0

    details = d_dao.get_student_detail_list(student_id)
    
    return render_template(
        'dashboard/leaning_pro.html',
        student_id=student_id,
        stats=stats,
        percent=percent,
        details=details
    )