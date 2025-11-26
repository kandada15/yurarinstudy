# Task モデルを MySQL (task テーブル) とやり取りする DAO クラス

import mysql.connector
from mysql.connector import MySQLConnection
from models.model_task import Task
from config.db_config import DB_CONFIG

class TaskDao:
  """ TaskテーブルにアクセスするためのDAOクラス """
  