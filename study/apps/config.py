from pathlib import Path

basedir = Path(__file__).parent.parent

# BaseConfigクラス
class BaseConfig:
    SECRET_KEY = "2AZSMss3p5OPbcY2hb5J" # セキュリティのための秘密鍵
    WTF_CSRF_SECRET_KEY = "Auwzsy2Su5usgKN7KZs6f" # CSRF対策のための秘密鍵

# BaseConfigクラスを継承してLocalConfigクラスを作成する
class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'local.sqlite'}" 
    # SQLAlchemyの変更追跡を無効にする
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    SQLALCHEMY_ECHO = True # SQLAlchemyのSQL文を表示する

# BaseConfigクラスを継承してTestingConfigクラスを作成する
class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'testing.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

# localhost3306 MySQLDBサーバーのデフォルト値
class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://dev_user@localhost:3306/dev_db"
    )  
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://prod_user@prod_server:3306/prod_db"
     )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
# config変数にマッピングする
config = {
    "testing": TestingConfig,
    "local": LocalConfig,
    "development": DevelopmentConfig,
    "production": ProductionConfig, 
}