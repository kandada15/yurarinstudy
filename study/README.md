# Flask Study Project

このプロジェクトは、Flask と MySQL を使用して作成する学習用システムです。  
Flask-Login による認証、を実装しています。

追加したライブラリなどは、以下に記入してください。記入した場合、コミットする時のコメントに記入などして共有するように。

---

## 1. 環境構築

### 1.1 仮想環境の作成（推奨）
```bash
# プロジェクトルートで実行
# 実行は、src/Flask/プロジェクト名（study）
python -m venv venv

## SCriptsフォルダに階層を移した後、実行
PowerShell Set-ExecutionPolicy RemoteSigned CurrentUser

### 仮想環境に入る


# サーバ起動（実行）
flask run

```

### 必要パッケージのインストール
```bash
pip install Flask
pip install Flask-SQLAlchemy #Textを持ってくる際に利用
pip install Flask-Migrate
pip install Flask-Login
pip install Flask-WTF
pip install pymysql #いらなくなりました。
pip install  mysql-connector-python
```

### マイグレーション　一応の記載
```bash
flask db init       # 初回のみ
flask db migrate -m "initial migration"
flask db upgrade
```

### DBについて  ←  使わなくなった。
```bash
# apps/config.py 内
SQLALCHEMY_DATABASE_URI = "sqlite:///local.sqlite"   # ローカル開発用
SQLALCHEMY_DATABASE_URI = "sqlite:///testing.sqlite" # テスト環境用

# DBの環境は.envファイル、("local")参照
## 中身を変更することで、環境を変更可能
FLASK_APP=apps.app:create_app("local")
FLASK_ENV=development
```

### フォルダに関すること
crud = ユーザ情報に関すること
auth = 新規登録
task = 課題機能
writing = ライティング機能

### 作業の進め方
Blueplintを利用する。
各機能は各フォルダ名を設定して、ファイルを作成して作業を進めます。

○ 階層例（大機能一つ分）
※記載されてないですが、views.pyなど「.py」は含まれています。
─task
│  ├─dao
│  │  └─__pycache__
│  ├─models
│  │  └─__pycache__
│  ├─static
│  │  ├─css
│  │  └─js
│  ├─templates
│  │  ├─task_admin
│  │  └─task_stu
│  └─__pycache__

○app.pyにて各アプリ(機能)と連携する。
例：
```bash
# アプリの連携
from apps.crud.views import crud_bp
app.register_blueprint(crud_bp, url_prefix='/crud')
```

○views.pyにてアプリの動きを書いていく。
例：
```bash
# 必要機能、DB必要情報のimport
from flask import Blueprint, render_template
from .dao.task_dao import TaskDao

# アプリの作成
task_bp = Blueprint(
  "task",
  __name__,
  template_folder="templates",
  static_folder="static"
)

# daoのインスタンス化
task_dao = TaskDao()

# 課題作成機能
@task_bp.route("/")
def task():
  task_list = task_dao.find_all()
  return render_template('task_admin/ass_create.html', task=task_list)
```











