from flask import Blueprint, render_template

# Blueprintの作成
auth_bp = Blueprint('auth', __name__, template_folder='templates')

# ルーティング定義
@auth_bp.route('/login')
def login():
    return "ここはログイン画面です（制作中）"