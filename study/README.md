# Flask Study Project

このプロジェクトは、Flask と MySQL を使用して作成する学習用システムです。  
Flask-Login による認証、Flask-Migrate によるマイグレーション機能を実装しています。

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
pip install Flask-SQLAlchemy
pip install Flask-Migrate
pip install Flask-Login
pip install Flask-WTF
pip install pymysql
```

### マイグレーション
```bash
flask db init       # 初回のみ
flask db migrate -m "initial migration"
flask db upgrade
```

### DBについて
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








