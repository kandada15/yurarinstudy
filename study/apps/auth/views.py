from flask import Blueprint, render_template, request, redirect, url_for, session
from apps.crud.models.model_admin import Admin 
from apps.crud.models.model_student import Student 

# Blueprintの作成
auth_bp = Blueprint(
    'auth',
    __name__,
    # 使用するテンプレートフォルダ
    template_folder='templates',
    # 専用の静的ファイル(CSS,JS,画像など)を置くフォルダ
    static_folder='static'
    )

# ルーティングの定義
# ログイン
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # エラーメッセージ初期値
    error = None

    # POST/ログインフォーム送信かどうか判定
    if request.method == 'POST':
        # 値を取得
        user_id = request.form.get('username')
        password = request.form.get('password')
        user_type = request.form.get('user_type')

        # 管理者ならAdmin,学生ならStudentテーブルから該当ユーザを取得
        if user_type == 'admin':
            user = Admin.query.filter_by(admin_id=user_id).first()
        else:
            user = Student.query.filter_by(student_id=user_id).first()

        # パスワードチェック
        if user and user.password == password:
            if user_type == 'admin':
                session['user_id'] = user.admin_id 
            else:
                # セッションに名前を保存
                session['user_id'] = user.student_id
            
            session['user_type'] = user_type
            if user_type == 'admin':
                session['user_name'] = user.admin_name
                # 管理者の場合はダッシュボード画面
                return redirect(url_for('dashboard.index'))
            else:
                session['user_name'] = user.student_name
                # 受講者の場合はマイページ画面
                return redirect(url_for('mypage.index'))
        else:
            error = 'ユーザ名またはパスワードに誤りがあります'
    return render_template('login.html', error=error)

# ログイン情報を削除しログイン画面へリダイレクト
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))