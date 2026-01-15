from flask import Flask
# extensions から db と csrf を読み込む
from apps.extensions import db, csrf

# アプリケーションの作成
app = Flask(__name__)

# データベース設定
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:20260210@localhost/study"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ" # 適当な文字列でOK

# db と csrf をアプリに連携（初期化）
db.init_app(app)
csrf.init_app(app)
# データベース設定
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:20260210@localhost/study"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ" # 適当な文字列でOK

# db と csrf をアプリに連携（初期化）
db.init_app(app)
csrf.init_app(app)

# -- 以下アプリとの連携 --
# Blueprintの登録
from apps.crud.views import crud_bp 
app.register_blueprint(crud_bp, url_prefix='/crud')

from apps.task.views import task_bp
app.register_blueprint(task_bp, url_prefix='/task')

from apps.dashboard.views import dashboard_bp
app.register_blueprint(dashboard_bp, url_prefix='/dashboard') 

from apps.writing.views import writing_bp
app.register_blueprint(writing_bp, url_prefix='/writing')