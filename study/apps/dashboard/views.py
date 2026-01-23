from flask import Blueprint, render_template, session, redirect, url_for
from apps.extensions import db
from apps.task.models.model_streamed import Streamed
from apps.task.models.model_submission import Submission
from apps.crud.models.model_admin import Admin
from apps.crud.models.model_group import Group
from apps.crud.models.model_task import TaskStreamed

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
    # セッション確認
    if 'user_id' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('auth.login'))

    login_admin_id = session['user_id']
    
    # 1. 管理者情報の取得
    admin = Admin.query.filter_by(admin_id=login_admin_id).first()
    
    # 2. 自分が担当するグループ一覧の取得
    groups = Group.query.filter_by(admin_id=login_admin_id).all()

    # 3. テンプレートに渡すデータ
    # ※DBに実在するカラム名（admin_name等）に合わせます
    return render_template(
        'dashboard/dashboard.html', 
        admin=admin, 
        groups=groups,
        streamed_count=10,    # 以下、まだロジックがないものは仮の数値
        unchecked_count=5,
        submitted_count=20,
        unsubmitted_count=2,
        weekly_deadline_count=1
    )

task_bp = Blueprint('task', __name__, template_folder='templates', static_folder='static')

@task_bp.route('/list')
def list():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    tasks = TaskStreamed.query.order_by(TaskStreamed.streamed_date.desc()).all()

    return render_template('task/deli_task_list.html', tasks=tasks)