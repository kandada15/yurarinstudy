from flask import Blueprint, render_template

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/login')
def login():
    return "ここはログイン画面です（制作中）"