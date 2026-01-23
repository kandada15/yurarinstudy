from flask import Flask
from apps.extensions import db, csrf
from apps.auth.views import auth_bp
from apps.crud.views import crud_bp 
from apps.task.views import task_bp
from apps.dashboard.views import dashboard_bp 
from apps.writing.views import writing_bp

# Flaskアプリ作成・初期化
def create_app():
    app = Flask(__name__)

    # DB設定
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:20260210@localhost/study"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ"

    # Flask拡張の初期化（db,csrfをアプリに紐づけ）
    db.init_app(app)
    csrf.init_app(app)

    # Blueprint登録
    app.register_blueprint(auth_bp, url_prefix='/auth') 
    app.register_blueprint(writing_bp, url_prefix='/writing')
    app.register_blueprint(crud_bp, url_prefix='/crud')
    app.register_blueprint(task_bp, url_prefix='/task')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard') 

    return app

# Flaskコマンドや実行時に使用するアプリインスタンス作成
app = create_app()