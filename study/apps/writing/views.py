from flask import Blueprint, redirect, render_template

# アプリの作成
writing = Blueprint(
  'writing',
  __name__,
  # 使用するフォルダ
  template_folder='templates',
  static_folder='static'
)

@writing.route('/')
def index():
  # templates/crud/index.htmlとなる
  return render_template('writing/index.html')

@writing.route('/')
def writing_top():
  # templates/crud/index.htmlとなる
  return render_template('writing/writing_top.html')