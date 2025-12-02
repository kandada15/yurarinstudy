from flask import Blueprint, redirect, render_template, abort
from apps.app import db 
from apps.writing.models import Category 

# アプリの作成 (省略なし)
writing = Blueprint(
  'writing',
  __name__,
  template_folder='templates',
  static_folder='static'
)


@writing.route('/')
def index():
  # templates/crud/index.htmlとなる
  return render_template('writing/index.html')

@writing.route('/')
def writing_top():
