import json
import os
import databases
import sqlalchemy
from employee_management.domain import constants

DATABASE = "mysql"

# SecretManagerから取得・マウントされたJSONファイルから認証情報を読み込む
if os.path.exists(constants.DB_SECRET_PATH):
    f = open(constants.DB_SECRET_PATH, 'r', encoding='utf-8')
    jsondata = json.load(f)
    f.close()

    USER = jsondata['DB_USER']
    PASSWORD = jsondata['DB_PASS']
    DB_NAME = jsondata['DB_NAME']
    HOST = jsondata['CONNECTION_DIST']
else:
    # ファイルが見つからない場合の環境変数フォールバック
    USER = os.getenv("DB_USER", "user")
    PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_NAME = os.getenv("DB_NAME", "employee_db")
    HOST = os.getenv("DB_HOST", "mysql:3306")

# databases ライブラリ用非同期接続URL (aiomysql)
DATABASE_URL = f"mysql+aiomysql://{USER}:{PASSWORD}@{HOST}/{DB_NAME}?charset=utf8mb4"

# databases.Database インスタンス（非同期DB接続プール）
database = databases.Database(DATABASE_URL, min_size=5, max_size=20)

ECHO_LOG = False
# SQLAlchemy Core Engine (同期マイグレーション・テーブル作成用)
ENGINE_URL = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DB_NAME}?charset=utf8mb4"
engine = sqlalchemy.create_engine(ENGINE_URL, echo=ECHO_LOG)
metadata = sqlalchemy.MetaData()
