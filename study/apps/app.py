from flask import Flask
# from flask_login import LoginManager
from apps.config import config
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

## 他アプリで利用できるように

# DBを他のアプリよりアクセス可能に
db = SQLAlchemy()
# CSRF対策
csrf = CSRFProtect()


### 以下コードは、ユーザー取得時に開放
## Loginmanager、create_app内のlogin_manager=init_app(app)も開放
# login_manager = LoginManager()
# 未ログイン時、実行したい関数を記入。
# login_manager.login_view = 'crud/index.html'


def create_app():
  # アプリケーション作成の準備
  app = Flask(__name__)

  # 上から、db, DBを使う準備、csrf対策、認証機能を適用
  db.init_app(app)
  Migrate(app, db)
  csrf.init_app(app)
  # login_manager.init_app(app)

  # -- 以下アプリとの連携 --
  from apps.crud import views as crud_views
  # crud_viewsのcrudとURL "/crud"を関連付ける
  app.register_blueprint(crud_views.crud, url_prefix='/crud')

  # ダッシュボードアプリ
  from apps.dashboard.views import dash_bp 
  app.register_blueprint(dash_bp, url_prefix='/dashboard')

  return app