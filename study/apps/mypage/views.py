from flask import Blueprint, render_template, session, redirect, url_for
from apps.mypage.dao.mypage_dao import MypageDao

mypage_bp = Blueprint('mypage', __name__, template_folder='templates', static_folder='static')
u_dao = MypageDao()

@mypage_bp.route('/')

# 管理者ID（a...）を弾く
@mypage_bp.before_request
def restrict_access():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    if user_id.startswith('a'):
        return redirect(url_for('dashboard.index'))

@mypage_bp.route('/')
def index():
    if 'student_id' not in session:
        return redirect(url_for('auth.login'))
    
    # セッションから student_id を取得
    student_id = session.get('student_id')
    profile = u_dao.get_user_profile(student_id)
    tasks = u_dao.get_task_summary(student_id)
    progress = u_dao.get_writing_progress(student_id)

    # 進捗率と円グラフの計算 (外周 251.2)
    comp = progress['completed'] or 0
    total = progress['total'] or 1
    percent = int((comp / total) * 100)
    stroke_offset = 251.2 * (1 - percent / 100)

    return render_template(
          'mypage/mypage.html', 
          user=profile, 
          tasks=tasks, 
          percent=percent, 
          offset=stroke_offset,
          comp=comp,
          total=total)