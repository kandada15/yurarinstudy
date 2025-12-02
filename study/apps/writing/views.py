from flask import Blueprint, render_template

from flask import Blueprint, redirect, render_template, abort
from apps.app import db 
from apps.writing.models import Category 

# アプリの作成 (省略なし)
writing_bp = Blueprint(
  'writing',
  __name__,
  template_folder='templates',
  static_folder='static',
  url_prefix="/writing"
)



@writing_bp.route('/')
def index():
  """ライティングトップ / カテゴリ一覧ページ"""
  return render_template('index.html')

@writing_bp.route('/step_list')
def step_list():
  """ステージ一覧ページ"""
  return render_template('step_list.html')

@writing_bp.route('/step_learning')
def step_learning():
  """ステージ一覧ページ"""
  return render_template('step_learning.html')

