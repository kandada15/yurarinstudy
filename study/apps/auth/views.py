from flask import Blueprint, render_template, request, redirect, url_for, session
from apps.extensions import db
from apps.crud.models.model_admin import Admin 
from apps.crud.models.model_student import Student 
from apps.writing.models.model_progress import Progress

# Blueprintの設定
# template_folder='templates' を指定することで apps/auth/templates を参照します
auth_bp = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # エラーメッセージの初期化
    error = None

    if request.method == 'POST':
        # フォーム（login.html）の各 input の name 属性から取得
        user_id = request.form.get('username')
        password = request.form.get('password')
        user_type = request.form.get('user_type') # 'student' か 'admin'

        # 1. ユーザータイプに応じて検索するテーブルを分岐
        if user_type == 'admin':
            # 管理者テーブルを検索
            user = Admin.query.filter_by(admin_id=user_id).first()
        else:
            # 受講者テーブルを検索
            user = Student.query.filter_by(student_id=user_id).first()

        # 2. ユーザーが存在し、パスワードが一致するか確認
        if user and user.password == password:
            session['user_id'] = user_id
            session['user_type'] = user_type
            
            if user_type == 'admin':
                session['user_name'] = user.admin_name
            else:
                session['user_name'] = user.student_name
            
            # 管理者ならダッシュボードへ、受講者ならライティング学習画面へ
            if user_type == 'admin':
                return redirect(url_for('dashboard.index'))
            else:
                return redirect(url_for('writing.index'))            
            
            # ログイン成功：ライティング学習のトップへリダイレクト
            return redirect(url_for('writing.index'))
        else:
            # ログイン失敗：エラーメッセージをセット
            error = 'ユーザ名またはパスワードに誤りがあります'
    return render_template('login.html', error=error)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))