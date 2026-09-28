import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 環境変数からDB接続設定を取得（デフォルトはローカルDocker Compose設定）
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "mysql")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "employee_db")

# MySQL接続URLの構築 (PyMySQLを使用)
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

# SQLAlchemy エンジンの作成
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False,
)

# セッションファクトリの定義
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORMモデルの基底クラス
Base = declarative_base()


def get_db():
    """DBセッションのコンテキスト管理用ジェネレータ関数"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
