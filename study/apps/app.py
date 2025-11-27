from flask import Flask
from flask_wtf.csrf import CSRFProtect

# CSRF対策
csrf = CSRFProtect()

# アプリケーション作成の準備
app = Flask(__name__)

# csrf対策を適応
csrf.init_app(app)

# -- 以下アプリとの連携 --
from apps.crud.views import crud_bp
app.register_blueprint(crud_bp, url_prefix='/crud')

from apps.task.views import task_bp
app.register_blueprint(task_bp, url_prefix='/task')

