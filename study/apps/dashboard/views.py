from flask import Blueprint, render_template, session, redirect, url_for
from apps.task.dao.streamed_dao import StreamedDao
from apps.task.dao.submission_dao import SubmissionDao2

dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates', static_folder='static')

# ---------------------------------------------------------
# ゲートキーパー機能: 生徒アカウントのアクセスを制限
# ---------------------------------------------------------
@dashboard_bp.before_request
def restrict_access():
    """
    ダッシュボード内の全てのルートに対し、実行前に権限チェックを行います。
    """
    user_id = session.get('user_id')
    
    # 1. 未ログインの場合はログイン画面へ飛ばす
    if not user_id:
        return redirect(url_for('auth.login'))
        
    # 2. IDが 's' で始まる(生徒)場合は、ダッシュボードに入れず学習トップへ飛ばす
    #
    if user_id.startswith('s'):
        return redirect(url_for('writing.index'))

# ---------------------------------------------------------
# ダッシュボード・メイン画面
# ---------------------------------------------------------
@dashboard_bp.route('/')
def index():
    """
    ここは管理者（IDが s で始まらないユーザー）だけが閲覧可能です。
    """
    admin_id = session.get('user_id')
    
    # DAOのインスタンス化
    s_dao = StreamedDao()
    sub_dao = SubmissionDao2()
    
    # 統計データの取得
    streamed_count = s_dao.get_streamed_count(admin_id)
    weekly_deadline = s_dao.get_weekly_deadline_count()
    sub_stats = sub_dao.get_stats()

    # 未提出数の簡易計算（配信数 - 提出数）
    unsubmitted_count = max(0, streamed_count - sub_stats["submitted_count"])

    return render_template(
        'dashboard/dashboard.html',
        admin={"admin_id": admin_id, "admin_name": session.get('user_name', '管理者')},
        groups=[], # グループ一覧が必要なら別途 GroupDao を作成
        streamed_count=streamed_count,
        unchecked_count=sub_stats["unchecked_count"],
        submitted_count=sub_stats["submitted_count"],
        unsubmitted_count=unsubmitted_count,
        weekly_deadline_count=weekly_deadline
    )