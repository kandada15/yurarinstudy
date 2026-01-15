# apps/config/db_config
 
# config/db_config.py
# MySQL の接続情報をまとめて管理するファイル
 
DB_CONFIG = {
    # MySQL サーバのホスト名
    # 自分のPCで動かしている場合は "localhost" のままでOK
    "host": "localhost",
 
    # MySQL のユーザー名（自分の環境に合わせて変更）
    "user": "root",
 
    # MySQL のパスワード（自分の環境に合わせて変更）
    "password": "20260210",
 
    # 利用するデータベース名
    # 例：CREATE DATABASE flask_sample; で作ったもの
    "database": "study2",
}