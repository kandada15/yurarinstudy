from flask import Blueprint, render_template, session, redirect, url_for
from apps.extensions import db
from apps.task.models.model_streamed import Streamed
from apps.task.models.model_submission import Submission
from apps.crud.models.model_admin import Admin
from apps.crud.models.model_group import Group
from datetime import datetime, timedelta

# Blueprintの作成
dashboard_bp = Blueprint(
    'dashboard', 
    __name__, 
    # 使用するテンプレートフォルダ
    template_folder='templates',
    # 専用の静的ファイル(CSS,JS,画像など)を置くフォルダ
    static_folder='static'
)

# ルーティングの定義
@dashboard_bp.route('/')
def index():
    """管理者ダッシュボード画面"""
    
    # 1. セッションからログイン中の管理者IDを取得
    # login_admin_id = session.get('user_id')

    # # ログインしていない場合はログイン画面へ強制リダイレクト
    # if not login_admin_id:
    #     return redirect(url_for('auth.login'))
    login_admin_id = session.get('user_id')
    # 2. ログイン中の管理者情報をDBから取得
    # 定義書の物理名に合わせて Admin.ADMIN_ID で検索
    admin_data = Admin.query.filter_by(admin_id=login_admin_id).first()

    # 万が一DBにデータがない場合の安全策
    # if not admin_data:
    #     session.clear() # セッションを破棄してログインへ
    #     return redirect(url_for('auth.login'))

    # 3. 担当グループ一覧の取得
    # 管理者IDに紐づくグループを取得
    groups = Group.query.filter_by(admin_id=login_admin_id).all()

    # 4. 統計データの集計
    
    # (1) 累計課題配信数
    streamed_count = TaskStreamed.query.count()

    # (2) 未添削課題数 (CHECK_FLAG が False のもの)
    # ※定義書に基づき物理名 CHECK_FLAG を参照
    unchecked_count = TaskSubmission.query.filter_by(check_flag=False).count()

    # (3) 提出済み件数 (SUBMIT_FLAG が True のもの)
    submitted_count = TaskSubmission.query.filter_by(submit_flag=True).count()

    # (4) 未提出件数 (仮の計算式：全配信数 - 提出済数 など)
    # ※本来は (受講生数 * 課題数) ですが、まずは固定値または簡易計算で実装
    unsubmitted_count = 8 # 必要に応じてロジックを追加

    # (5) 今週の締切課題数
    today = datetime.now()
    one_week_later = today + timedelta(days=7)
    # STREAMED_LIMIT が今日から1週間以内のものをカウント
    weekly_deadline_count = TaskStreamed.query.filter(
        TaskStreamed.streamed_limit.between(today, one_week_later)
    ).count()

    # 5. テンプレートへすべてのデータを渡してレンダリング
    return render_template(
        'dashboard/dashboard.html',
        admin=admin_data,
        groups=groups,
        streamed_count=streamed_count,
        unchecked_count=unchecked_count,
        submitted_count=submitted_count,
        unsubmitted_count=unsubmitted_count,
        weekly_deadline_count=weekly_deadline_count
    )