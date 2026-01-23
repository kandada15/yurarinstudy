from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

# 拡張機能オブジェクト作成
db = SQLAlchemy()
# CSRF(保護機能)追加
csrf = CSRFProtect()